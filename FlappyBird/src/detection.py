# 目标检测
import cv2

# 加载预训练的 Haar 特征分类器文件
cascade_file = 'path/to/haarcascade_frontalface_default.xml'  # 替换为实际的文件路径
cascade = cv2.CascadeClassifier(cascade_file)

# 加载图像
image_file = 'path/to/image.jpg'  # 替换为实际的图像文件路径
image = cv2.imread(image_file)

# 转换图像为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用 Haar 特征分类器进行目标检测
objects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# 在图像上标记检测到的目标
for (x, y, w, h) in objects:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# 显示结果图像
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()