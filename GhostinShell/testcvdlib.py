# -*- coding: utf-8 -*-

import cv2  
import dlib
import time

detector=dlib.get_frontal_face_detector()

def resize_width(image, num):
	height, width = image.shape[:2]  
	size = (int(width*num), int(height*num))  
	resized = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
	return resized

def rect_to_bb(rect):
	x = rect.left()
	y = rect.top()
	w = rect.right() - x 
	h = rect.bottom() - y 
	return (x, y, w, h)

def fast_face_finder(image, zoom):
	raw_size = image.shape

	image = resize_width(image, zoom)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 0)
	
	i = 0
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

mask = cv2.imread("facemask.png", cv2.IMREAD_UNCHANGED)

GAP = 2
ZOOM = 1.0
WIDTH = 240
HEIGHT = 320
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
fps =cap.get(cv2.CAP_PROP_FPS) 
cnt = GAP
time0 = time.time()
while(1):
	ret, frame = cap.read()
	cv2.putText(frame, "FPS: {}".format(1.0/(time.time()-time0)), (100, 50),
		cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
	time0 = time.time()
	if GAP==cnt:
		faces = fast_face_finder(frame, ZOOM)
		cnt = 0
	cnt = cnt + 1
	i = 0
	for face in faces:
		x=face["x"]
		y=face["y"]
		w=face["width"]
		h=face["height"]
		if x < 0: x = 0
		if y < 0: y = 0
		if (x+w) > WIDTH: w = WIDTH - x - 1 
		if (y+h) > HEIGHT: h = HEIGHT - y - 1
		smileface = cv2.resize(mask, (w, h), interpolation=cv2.INTER_AREA)
		for ii in range(y,y+h):
			for kk in range(x,x+w):
				if smileface[ii - y, kk - x][3] != 0:
					frame[ii,kk]=smileface[ii - y, kk - x ][0:3]

		i = i + 1
	cv2.imshow("capture", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows() 
