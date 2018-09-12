#encoding:utf-8
#!/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os
import base64
import datetime
import random
import cv2
import numpy as np
import json
import requests
from os import environ

app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])

@app.route('/')
def home():
	rt = { "path":"/distance" }
	return jsonify(rt)

@app.route('/distance')
def upload_test():
	return render_template('distance.html')

@app.route('/detect')
def detect():
	return render_template('detect.html')

@app.route('/post2detect', methods=['POST'], strict_slashes=False)
def post_detect():
	f = request.files['photo1']
	f.save("3.jpg")
	with open("3.jpg", 'rb') as f7:
		_byte1 = f7.read()
	image_str1 = base64.b64encode(_byte1)
	
	url = 'http://localhost:65530/api/face/detect/'
	body = {"image_base64": image_str1} 
	rt = requests.post(url, data=body)
	print(rt.text)
	jsonData = json.loads(rt.text)
	if jsonData.get("ok")==False:
		return rt.text
	image = cv2.imread("3.jpg", cv2.IMREAD_COLOR)
	face_num = 0
	rects = jsonData.get("face")
	for (i, rect) in enumerate(rects):
		face_num = face_num + 1

		x=rect['x']
		y=rect['y']
		w=rect['width']
		h=rect['height']

		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

		cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	cv2.imwrite("templates\\3.jpg", image)
	return render_template('detectSuccess.html')


@app.route('/post2distance', methods=['POST'], strict_slashes=False)
def api_upload():
	f = request.files['photo1']
	f.save("1.jpg")
	with open("1.jpg", 'rb') as f7:
		_byte1 = f7.read()
	image_str1 = base64.b64encode(_byte1)

	f = request.files['photo2']
	f.save("2.jpg")
	with open("2.jpg", 'rb') as f7:
		_byte2 = f7.read()
	image_str2 = base64.b64encode(_byte2)

	url = 'http://localhost:65530/api/face/distance/'
	body = {"image1_base64": image_str1,"image2_base64":image_str2} 
	rt = requests.post(url, data=body)
	return rt.text
 
if __name__ == '__main__':
	HOST = environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(environ.get('SERVER_PORT', '5559'))
	except ValueError:
		PORT = 65530

	#多线程模式
	#app.run(HOST, PORT, threaded=True)

	#多进程模式
	#app.run(HOST, PORT, processes=3)

	app.run(HOST, PORT, debug=True)