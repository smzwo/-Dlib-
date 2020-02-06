import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import joblib
import cv2  # 图像处理的库OpenCv
import get_detector
import learning_face

class face_emotion():
    def getdetector(self):
        get_detector.get_detector(self)
    def learningface(self):
        learning_face.learning_face(self)
