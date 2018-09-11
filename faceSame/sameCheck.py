import sys
import os
import dlib
import cv2
import cmath

predictor_path = 'shape_predictor_5_face_landmarks.dat'
# face_rec_model_path = sys.argv[2]
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
img1_name = sys.argv[1]
img2_name = sys.argv[2]


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

img1 = cv2.imread(img1_name)
# cv2.imshow("test", img1)
# cv2.waitKey()
dets = detector(img1, 1)
print("Number of faces detected: {}".format(len(dets)))

for k, d in enumerate(dets):
    shape = sp(img1, d)
    face_descriptor0 = facerec.compute_face_descriptor(img1, shape)










img2 = cv2.imread(img2_name)
dets = detector(img2, 1)
print("Number of faces detected: {}".format(len(dets)))

for k, d in enumerate(dets):
    shape = sp(img2, d)
    face_descriptor1 = facerec.compute_face_descriptor(img2, shape)







distance = 0.0
for i in range(128):
    distance = distance + (face_descriptor0[i]-face_descriptor1[i])*(face_descriptor0[i]-face_descriptor1[i])
distance = cmath.sqrt(distance).real
print (distance) 
if (distance <= 0.4000000001):
    print ("Must Same People")
    exit()
if (distance <= 0.5000000001):
    print ("Maybe Same People")
    exit()
print ("not same People")