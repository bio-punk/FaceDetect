from webFaceD import app
from flask import jsonify
from flask import request

from webFaceD import detector
import cv2

from .Image import base64_2RGB
from .Image import resize_width
from .Image import rect_to_bb

def std_face_finder(image, zoom):
	raw_size = image.shape

	image = resize_width(image, zoom)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	
	faces = []
	for rect in rects:
		(x, y, w, h) = rect_to_bb(rect)
		face = {
			"x":int(x/zoom),
			"y":int(y/zoom),
			"width":int(w/zoom),
			"height":int(h/zoom)
		}
		faces.append(face)
	return faces

@app.route('/api/face/detect/', methods=['GET'])
def get_detect():
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
				}
			]
		}
	}

	return jsonify(rt)

@app.route('/api/face/detect/', methods=['POST'])
def post_detect():
	imageB64Str = request.form['image_base64']
	image = base64_2RGB(imageB64Str)

	faces = std_face_finder(image, 1.57)
	
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