
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

from flask_api import FlaskAPI
app = FlaskAPI(__name__)

import webFaceD.views

import cv2
import dlib

detector=dlib.get_frontal_face_detector()
shape_predictor_5p = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
shape_predictor_68p = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# cnn_detector = dlib.cnn_face_detection_model_v1("mmod_human_face_detector.dat")

import webFaceD.api