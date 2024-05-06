# 目标检测
import cv2
import numpy as np

import cv2

# 加载 Haar 特征分类器模型文件
cascade_file = 'D:\Program Files\Python39\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml'  # 替换为实际的文件路径
face_cascade = cv2.CascadeClassifier(cascade_file)

# 加载图像文件
image_file = '../resources/crowd.jpg'  # 替换为实际的图像文件路径
image = cv2.imread(image_file)

# 转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用 Haar 特征分类器进行人脸检测
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# 绘制检测结果
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)

# 显示检测结果
cv2.imshow('Face Detection Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
