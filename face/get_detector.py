import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import joblib
import cv2  # 图像处理的库OpenCv


def get_detector(self):
    # 使用特征提取器get_frontal_face_detector
    self.detector = dlib.get_frontal_face_detector()
    # dlib的68点模型，使用作者训练好的特征预测器
    self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    # 建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
    self.cap = cv2.VideoCapture(0)
    # 设置视频参数，propId设置的视频参数，value设置的参数值
    self.cap.set(3, 144)
    # 截图screenshoot的计数器
    self.cnt = 0