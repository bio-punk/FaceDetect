from webFaceD import app
from flask import jsonify
from flask import request

from webFaceD import cnn_detector

from .Image import base64_2RGB
from .Image import resize_width
from .Image import rect_to_bb

def cnn_face_finder(image, zoom):
	raw_size = image.shape

	image = resize_width(image, zoom)

	dets = cnn_detector(image, 1)

	faces = []
	for i, det in enumerate(dets):
		rect = det.rect
		(x, y, w, h) = rect_to_bb(rect)
		face = {
			"x":int(x/zoom),
			"y":int(y/zoom),
			"width":int(w/zoom),
			"height":int(h/zoom),
			"confidence":det.confidence
		}
		faces.append(face)
	return faces

@app.route('/api/face/cnndetect/', methods=['GET'])
def get_cnndetect():
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
					"confidence":"float"
				}
			]
		}
	}

	return (rt)

@app.route('/api/face/cnndetect/', methods=['POST'])
def post_cnndetect():
	# imageB64Str = request.form['image_base64']
	imageB64Str = str(request.data.get("image_base64"))
	image = base64_2RGB(imageB64Str)

	faces = cnn_face_finder(image, 1.0)

	if len(faces) < 1:
		rt = """{
			"ok":False,
			"face":[]
		}"""
		print("hehe")
		return jsonify(rt)

	rt = { 
		"ok":True,
		"face":faces
	}

	return jsonify(rt)