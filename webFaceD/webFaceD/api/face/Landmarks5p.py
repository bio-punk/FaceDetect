from webFaceD import app
from flask import jsonify
from flask import request

from webFaceD import detector
from webFaceD import shape_predictor_5p
import cv2
import numpy as np

from .Image import base64_2RGB
from .Image import resize_width
from .Image import rect_to_bb
from .Image import shape_to_np

def face_shape_dete(image, zoom):
	raw_size = image.shape

	image = resize_width(image, zoom)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	
	faces = []
	for rect in rects:
		(x, y, w, h) = rect_to_bb(rect)
		shape = shape_predictor_5p(gray, rect)

		face_shape_list = []
		for i in range(0, 5):
			face_shape_list.append({"x":int(shape.part(i).x / zoom),"y":int(shape.part(i).y / zoom)})
		face = {
			"x":int(x/zoom),
			"y":int(y/zoom),
			"width":int(w/zoom),
			"height":int(h/zoom),
			"face_shape_list":face_shape_list
		}
		faces.append(face)
	return faces

@app.route('/api/face/landmarks5p/', methods=['GET'])
def get_landmarks5p():
	rt = {
		"what you post":
		{
			"image_base64":"your image string that encoded by base64"
		},
		"what you get post":
		{
			"ok":False,
			"face":[
				{
					"x":"int",
					"y":"int",
					"height":"int",
					"width":"int",
					"face_shape_list":[
						{
							"x":"int",
							"y":"int"
						},
						{
							"x":"int",
							"y":"int"
						},
						{
							"x":"int",
							"y":"int"
						},
						{
							"x":"int",
							"y":"int"
						},
						{
							"x":"int",
							"y":"int"
						}
					]
				}
			]
		}
	}

	return jsonify(rt)

@app.route('/api/face/landmarks5p/', methods=['POST'])
def post_landmarks5p():
	imageB64Str = request.form['image_base64']
	image = base64_2RGB(imageB64Str)

	faces = face_shape_dete(image, 10.0)
	
	if len(faces) < 1:
		rt = """{
			"ok":False,
			"face":[]
		}"""
		return rt,404

	rt = { 
		"ok":True,
		"face":faces
	}

	return jsonify(rt)