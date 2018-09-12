from webFaceD import app
from flask import jsonify

@app.route('/api/face')
@app.route('/api/face/')
def face_api():
	rt = {
		"app 0":[
			"detect",
			"/api/face/detect"
		],
		"app 1":[
			"cnndetect",
			"/api/face/cnndetect"
		],
		"app 2":[
			"landmarks5p",
			"/api/face/landmarks5p"
		],
		"app 3":[
			"landmarks68p",
			"/api/face/landmarks68p"
		],
		"app 5":[
			"distance",
			"/api/face/distance"
		]
	}
	return (rt)