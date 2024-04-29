# 截取游戏画面
import datetime
import os
import time
import webbrowser

import numpy as np
from selenium import webdriver
from utils import get_webdriver, save_screenshot
from utils import get_game_window
import cv2

# 输入网址
# url = input("Enter your web url: ")
url = "https://flappybird.io/"

# 获取 WebDriver 实例并访问网页
driver = get_webdriver(url)

# 获取游戏窗口的位置和大小
# game_window = driver.find_element_by_class_name('flappy bird')
game_window = get_game_window(driver)

# 获取游戏窗口的位置和大小信息
location = game_window.location
size = game_window.size

print('location{}, size{}', location, size)


while True:
    # 获取游戏窗口的截图
    screenshot = driver.get_screenshot_as_png()
    save_screenshot(screenshot, 'screenshot')

    # 将二进制数据转换成 OpenCV 图像格式
    nparr = np.frombuffer(screenshot, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 截取游戏窗口的图像
    # game_frame = img_np[location['y']:location['y'] + size['height'], location['x']:location['x'] + size['width']]
    # 截取游戏窗口的图像
    game_frame = img_np[location['y']:location['y'] + size['height'], location['x']:location['x'] + size['width']]

    # 创建窗口并设置大小
    cv2.namedWindow('Game Frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Game Frame', size['width'], size['height'])

    # 显示截取的图像
    cv2.imshow('Game Frame', game_frame)
    key = cv2.waitKey(1)  # 检测键盘输入，参数表示每次等待键盘输入的毫秒数

    # 如果按下 ESC 键或窗口关闭按钮，则退出循环
    if key == 27 or key == ord('q'):
        break

# 关闭 OpenCV 窗口
cv2.destroyAllWindows()

# 关闭浏览器
driver.quit()
