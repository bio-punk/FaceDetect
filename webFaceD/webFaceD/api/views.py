from webFaceD import app
from flask import jsonify

@app.route('/api')
def hello_api():
	rt = {
		"api 0":[
			"face",
			"/api/face"
		]
	}
	return (rt)