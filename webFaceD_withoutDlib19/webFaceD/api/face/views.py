from webFaceD import app
from flask import jsonify

@app.route('/api/face')
def face_api():
	rt = {
		"app 0":[
			"detect",
			"/api/face/detect"
		],
		"app 1":[
			"cnndetect",
			"/api/face/cnndetect"
		]
	}
	return jsonify(rt)