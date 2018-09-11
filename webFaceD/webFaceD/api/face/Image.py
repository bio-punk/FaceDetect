import cv2
import base64
import numpy as np

def base64_2RGB(imgB64Str):
	imageStr = base64.b64decode(imgB64Str)
	npArr = np.fromstring(imageStr, np.uint8)  
	image = cv2.imdecode(npArr,cv2.COLOR_BGR2RGB) 
	return image

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

def shape_to_np(shape, pointNumber=68, dtype="int"):
    coords = np.zeros((pointNumber, 2), dtype=dtype)
    for i in range(0, pointNumber):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords