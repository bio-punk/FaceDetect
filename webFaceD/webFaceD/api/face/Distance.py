from webFaceD import app
from flask import jsonify
from flask import request
from cmath import sqrt

from webFaceD import detector
from webFaceD import shape_predictor_5p
from webFaceD import facerec
import cv2
import numpy as np

from .Image import base64_2RGB
from .Image import resize_width
from .Image import rect_to_bb

def calc_dis(img1, img2):
	dets1 = detector(img1, 1)
	dets2 = detector(img2, 1)
	totalFace = len(dets1) + len(dets2)
	if totalFace > 2 : return 501, -1.0
	if totalFace < 2 : return 502, -1.0

	shape = shape_predictor_5p(img1, dets1[0])
	face_descriptor0 = facerec.compute_face_descriptor(img1, shape)

	shape = shape_predictor_5p(img2, dets2[0])
	face_descriptor1 = facerec.compute_face_descriptor(img2, shape)

	distance = 0.0
	for i in range(128):
		distance = distance + (face_descriptor0[i]-face_descriptor1[i])*(face_descriptor0[i]-face_descriptor1[i])
	return 0, sqrt(distance).real


@app.route('/api/face/distance/', methods=['GET'])
def get_distance():
	"""
status_code 501:脸太多
status_code 502:脸太少
distance>0.5     - 不是一个人
0.4≤distance≤0.5 - 可能是一个人
distance<0.4     - 是同一个人
	"""
	rt = {
		"what you post":
		{
			"image1_base64":"your image string that encoded by base64",
			"image2_base64":"your image string that encoded by base64"
		},
		"what you get post":
		{
			"ok":False,
			"status_code":"if 'ok' is False",
			"distance":"float"
		}
	}

	return (rt)

@app.route('/api/face/distance/', methods=['POST'])
def post_distance():
	image1B64Str = str(request.data.get("image1_base64"))
	image2B64Str = str(request.data.get("image2_base64"))

	image1 = base64_2RGB(image1B64Str)
	image2 = base64_2RGB(image2B64Str)

	code, distance = calc_dis(image1, image2)
	
	if code != 0:
		rt = {
			"ok":False,
			"status_code":code,
			"distance":distance
		}
		return jsonify(rt)

	rt = { 
		"ok":True,
		"distance":distance
	}

	return jsonify(rt)