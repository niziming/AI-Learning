# 目标检测
import cv2
import numpy as np

# 加载游戏画面和小鸟模板
game_screen = cv2.imread('../resources/game_frame.png')
bird_template = cv2.imread('../resources/bird.png')

# 使用模板匹配算法
result = cv2.matchTemplate(game_screen, bird_template, cv2.TM_CCOEFF_NORMED)

# 设置匹配阈值
threshold = 0.8
locations = np.where(result >= threshold)

# 绘制检测结果
for pt in zip(*locations[::-1]):
    cv2.rectangle(game_screen, pt, (pt[0] + bird_template.shape[1], pt[1] + bird_template.shape[0]), (0, 255, 255), 1)

# 显示检测结果
cv2.imshow('Detection Result', game_screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
