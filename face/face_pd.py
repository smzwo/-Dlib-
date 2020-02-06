
import joblib
import cv2  # 图像处理的库OpenCv
import music

def face_pd(im_rd,a,b,c,d,dd,e):
    if (e < 0.02):#如果眼睛睁开距离与识别框高度之比小于0.2，则判定为闭眼，认为驾驶员疲劳驾驶
        cv2.putText(im_rd, "tired", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2, 4)
        #music.runtired()#播放提示音，提醒驾驶员注意
    else:
        cld = joblib.load("新最后最后最后五围2knn.m")#调用已经训练好的模型
        #  cld = joblib.load("新最后最后最后六围2knn.m")

        x = [[a, b, c, dd, e]]
        # 存储特征值
        # a-嘴巴宽度与识别框宽度之比
        # b-嘴巴高度与识别框高度之比
        # c-眉毛高度占比
        # dd-眉毛距离占比
        # e-眼睛睁开程度
        kll = int(cld.predict(x))#用训练好的KNN模型对获取的特征值进行分析分类，返回分类后的标签
        #根据标签判断当前表情，并在图像上输出
        emo=['angry','sadness','nature','nature','happy','normal','surprise']
        cv2.putText(im_rd, emo[kll-1], (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 0), 2, 4)

