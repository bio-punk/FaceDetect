# -*- coding: utf-8 -*-
 
import requests
import json
import base64
import cv2
import time
import dlib
from jinja2 import Template
import urllib
import numpy as np

# import urllib2

def draw(rects, image_name='test.png', windowName='window0'):
	image = cv2.imread(image_name, cv2.IMREAD_COLOR)
	face_num = 0
	for (i, rect) in enumerate(rects):
	    face_num = face_num + 1

	    x=rect['x']
	    y=rect['y']
	    w=rect['width']
	    h=rect['height']

	    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

	    cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
	            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

	cv2.imshow(windowName, image)

timebegin = time.time()
url = 'http://localhost:5555/api/face/detect/'

with open('test.png', 'rb') as f:
	_byte = f.read()

image_str = base64.b64encode(_byte)
body = {"image_base64": image_str} 

time1=time.time()
rt = requests.post(url, data=body)
time2=time.time()

print (rt.text)
timeend= time.time()
jsonData = json.loads(rt.text)

print ("requests time:{}".format(time2-time1))
print ("totaltime:{}".format(timeend-timebegin))

if jsonData.get("ok")==False:
	print("no face")
else:
	draw(jsonData.get("face"), image_name='test.png', windowName = "detect_homorua")
print ("_____________________________")

timebegin = time.time()
url = 'http://localhost:5555/api/face/detect/'

with open('test2.png', 'rb') as f:
	_byte = f.read()

image_str = base64.b64encode(_byte)
body = {"image_base64": image_str} 

time1=time.time()
rt = requests.post(url, data=body)
time2=time.time()

print (rt.text)
timeend= time.time()
jsonData = json.loads(rt.text)

print ("requests time:{}".format(time2-time1))
print ("totaltime:{}".format(timeend-timebegin))

if jsonData.get("ok")==False:
	print("no face")
else:
	draw(jsonData.get("face"), image_name='test2.png', windowName = "detect3p")
print ("_____________________________")

cv2.waitKey(0)

# GAP = 30
# ZOOM = 0.5
# WIDTH = 640
# HEIGHT = 480
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# fps =cap.get(cv2.CAP_PROP_FPS) 
# cnt = GAP
# while(1):
# 	ret, frame = cap.read()
# 	cv2.putText(frame, "FPS: {}".format(fps), (100, 50),
# 		cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# 	if GAP==cnt:
# 		time0 = time.time()
# 		rows = frame.shape[0]
# 		cols = frame.shape[1]
# 		channels = frame.shape[2]
# 		image_str = []
# 		for k in range(2, 0, -1):
# 			for step in range(0,rows):
# 				# for step2 in range(0,cols):
# 				image_str = image_str + frame[step, : ,k]

# 		# faces = fast_face_finder(frame, ZOOM)
# 		cnt = 0
# 	cnt = cnt + 1
# 	i = 0
# 	# for face in faces:
# 	# 	x=face["x"]
# 	# 	y=face["y"]
# 	# 	w=face["width"]
# 	# 	h=face["height"]
# 	# 	print "x={},y={},w={},h={}".format(x, y, w, h)
# 	# 	if (x+w) > WIDTH: w = WIDTH - x
# 	# 	if (y+h) > HEIGHT: h = HEIGHT - y
# 	# 	frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# 	# 	cv2.putText(frame, "Face #{}".format(i + 1), (x - 10, y - 10),
# 	# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
# 	# 	# smileface = cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA)
# 	# 	# frame[y:y+h, x:x+w]=smileface
# 	# 	i = i + 1  
# 	cv2.imshow("capture", frame)

# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break
# cap.release()
# cv2.destroyAllWindows() 