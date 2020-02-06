import dlib  # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import joblib
import cv2  # 图像处理的库OpenCv
import face_pd


def learning_face(self):
    # 眉毛直线拟合数据缓冲
    line_brow_x = []
    line_brow_y = []
    self.cap.set(3, 480)
    # self.cap.set(4, 640)
    # cap.isOpened（） 返回true/false 检查初始化是否成功
    while (True):

        # cap.read()
        # 返回两个值：
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵
        flag, im_rd = self.cap.read()

        # 每帧数据延时1ms，延时为0读取的是静态帧
        k = cv2.waitKey(30)
        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
        # 使用人脸检测器检测每一帧图像中的人脸。并返回人脸数rects
        faces = self.detector(img_gray, 0)
        # 待会要显示在屏幕上的字体
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 如果检测到人脸
        if (len(faces) != 0):
            # 对每个人脸都标出68个特征点
                # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
            for k, d in enumerate(faces):
                # 用红色矩形框出人脸
                cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                # print(d.top())
                # 计算人脸热别框边长
                self.face_width = d.right() - d.left()
                # 使用预测器得到68点数据的坐标
                shape = self.predictor(im_rd, d)
                # 圆圈显示每个特征点
                for i in range(17,27):
                    cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (214, 238, 247), -1, 8)
                for i in range(36,68):
                    cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 2, (214, 238, 247), -1, 8)
                    # cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                for i in range(18,22):#眉毛连线
                    cv2.line(im_rd, (shape.part(i).x, shape.part(i).y), (shape.part(i-1).x, shape.part(i-1).y), (214, 238, 247))
                    cv2.line(im_rd, (shape.part(i+5).x, shape.part(i+5).y), (shape.part(i+4).x, shape.part(i+4).y), (214, 238, 247))
                for i in range(36,42):#眼睛连线
                    if i==36:
                        cv2.line(im_rd, (shape.part(36).x, shape.part(36).y),(shape.part(41).x, shape.part(41).y), (214, 238, 247))
                        cv2.line(im_rd, (shape.part(42).x, shape.part(42).y), (shape.part(47).x, shape.part(47).y),(214, 238, 247))
                        continue
                    cv2.line(im_rd, (shape.part(i).x, shape.part(i).y), (shape.part(i-1).x, shape.part(i-1).y), (214, 238, 247))
                    cv2.line(im_rd, (shape.part(i+6).x, shape.part(i+6).y), (shape.part(i+5).x, shape.part(i+5).y), (214, 238, 247))
                for i in range(49,60):#嘴巴外圈连线
                    if i==59:
                        cv2.line(im_rd, (shape.part(59).x, shape.part(59).y),(shape.part(48).x, shape.part(48).y), (214, 238, 247))
                    cv2.line(im_rd, (shape.part(i).x, shape.part(i).y), (shape.part(i - 1).x, shape.part(i - 1).y),(214, 238, 247))
                # 分析任意n点的位置关系来作为表情识别的依据
                for i in range(61,68):#嘴巴内圈连线
                    if i==67:
                        cv2.line(im_rd, (shape.part(67).x, shape.part(67).y),(shape.part(60).x, shape.part(60).y), (214, 238, 247))
                    cv2.line(im_rd, (shape.part(i).x, shape.part(i).y), (shape.part(i - 1).x, shape.part(i - 1).y),(214, 238, 247))
                mouth_width = (shape.part(54).x - shape.part(48).x) / self.face_width  # 嘴巴咧开程度
                mouth_higth = (shape.part(66).y - shape.part(62).y) / self.face_width  # 嘴巴张开程度
                a = round(mouth_width, 10)
                b = round(mouth_higth, 10)
                # print("嘴巴宽度与识别框宽度之比：", mouth_width)
                # print("嘴巴高度与识别框高度之比：", mouth_higth)
                # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                brow_sum = 0  # 高度之和
                frown_sum = 0  # 两边眉毛距离之和
                for j in range(17, 21):
                    brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                    frown_sum += shape.part(j + 5).x - shape.part(j).x
                    line_brow_x.append(shape.part(j).x)
                    line_brow_y.append(shape.part(j).y)
                # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                tempx = np.array(line_brow_x)
                # print(tempx)
                tempy = np.array(line_brow_y)
                # print(tempy)
                #    if (len(line_brow_y) >= 20 or len(line_brow_x) >= 20):
                #        line_brow_x = []
                #        line_brow_y = []
                z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                # print(z1)
                self.brow_k = -round(z1[0], 3)  # 拟合出曲线的斜率和实际眉毛的倾斜方向是相反的
                brow_hight = (brow_sum / 10) / self.face_width  # 眉毛高度占比
                brow_width = (frown_sum / 5) / self.face_width  # 眉毛距离占比
                f = self.brow_k
                c = round(brow_hight, 10)
                dd = round(brow_width, 310)
                # 眼睛睁开程度
                eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y +
                           shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
                eye_hight = (eye_sum / 4) / self.face_width
                e = round(eye_hight, 10)
                # print("眼睛睁开距离与识别框高度之比：",round(eye_open/self.face_width,3))
                # 分情况讨论
                # 张嘴，可能是开心或者惊讶
                face_pd.face_pd(im_rd,a,b,c,faces[k],dd,e)
            # 标出人脸数
            cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # 没有检测到人脸
            cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        # 添加说明
        im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        im_rd = cv2.putText(im_rd, "ESC: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
        # 按下s键截图保存
        if (cv2.waitKey(100) & 0xFF == ord('S')):
            self.cnt += 1
            cv2.imwrite("screenshoot" + str(self.cnt) + ".jpg", im_rd)

        # 按下ESC键退出
        if (cv2.waitKey(100) & 0xFF == 27):
            break
        # 窗口显示
        cv2.imshow("camera", im_rd)
    # 释放摄像头
    self.cap.release()
    # 删除建立的窗口
    cv2.destroyAllWindows()