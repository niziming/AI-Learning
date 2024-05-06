# 工具函数
import datetime
import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_webdriver(url):
    # 检查浏览器类型
    # browser_type = input("Enter browser type (chrome/edge): ")
    browser_type = "edge"
    if browser_type.lower() == 'chrome':
        # ChromeDriver 可执行文件路径
        chrome_driver_path = 'path/to/chromedriver.exe'
        # 启动 Chrome 浏览器并访问网页
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
    elif browser_type.lower() == 'edge':
        # EdgeDriver 可执行文件路径
        edge_driver_path = 'D:\Program Files\edgedriver_win64\msedgedriver.exe'

        # 创建 EdgeOptions 对象
        edge_options = webdriver.EdgeOptions()

        edge_options.add_argument("--disable-popup-blocking")  # 禁用弹出框
        # edge_options.add_argument("--auto-open-devtools-for-tabs")  # 自动打开开发者工具
        edge_options.add_argument("--disable-infobars")  # 禁用信息栏
        edge_options.add_argument("--disable-extensions")  # 禁用扩展
        # edge_options.add_argument("--start-maximized")  # 启动时最大化窗口
        edge_options.add_argument("--force-device-scale-factor=1")
        # 设置浏览器窗口大小
        edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口

        # 启动 Edge 浏览器并传入选项
        driver = webdriver.Edge(executable_path=edge_driver_path, options=edge_options)
        # 设置浏览器窗口大小为固定尺寸
        driver.set_window_size(1020, 680)  # 例如设置为1920x1080像素
    else:
        raise ValueError("Unsupported browser: {}".format(browser_type))

    # 访问网页
    driver.get(url)

    return driver


def get_game_window(driver):
    try:
        # 等待游戏窗口加载完成页面的HTML元素
        game_window = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'testCanvas'))
        )
        if game_window is None:
            print("Game window not found.")
            driver.quit()
            sys.exit()
        # else:
        #     print("Game window found:", game_window)
    except TimeoutException as e:
        print("Timed out waiting for game window to load:", e)
        driver.quit()
        sys.exit()
    except Exception as e:
        print("Failed to find game window:", e)
        driver.quit()
        sys.exit()

    return game_window


def save_screenshot(screenshot, prefix):
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(__file__))

    # 拼接保存截图的完整路径
    filename = os.path.join(project_root, "resources", prefix + str(int(time.time())) + ".png")

    # 保存截图
    with open(filename, 'wb') as f:
        f.write(screenshot)

    print(filename)
    return filename


import cv2
import numpy as np


# 状态提取
def extract_game_state(game_screen):
    # 使用颜色过滤和图像处理方法提取游戏状态信息
    # 这里可以根据具体游戏画面的特点进行自定义，例如使用颜色过滤、边缘检测等方法

    # 示例：假设游戏画面中只有两种颜色，分别代表小鸟和管道，可以通过颜色过滤来提取它们的位置信息

    # 颜色过滤：假设小鸟的颜色为红色，管道为绿色
    lower_bird_color = np.array([170, 100, 100])  # 小鸟颜色的下限值
    upper_bird_color = np.array([180, 255, 255])  # 小鸟颜色的上限值
    lower_pipe_color = np.array([40, 100, 100])  # 管道颜色的下限值
    upper_pipe_color = np.array([80, 255, 255])  # 管道颜色的上限值

    # 将游戏画面转换为 HSV 色彩空间
    hsv = cv2.cvtColor(game_screen, cv2.COLOR_BGR2HSV)

    # 进行颜色过滤
    mask_bird = cv2.inRange(hsv, lower_bird_color, upper_bird_color)
    mask_pipe = cv2.inRange(hsv, lower_pipe_color, upper_pipe_color)

    # 找到小鸟的位置信息
    bird_contours, _ = cv2.findContours(mask_bird, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if bird_contours:
        bird_x, bird_y, bird_w, bird_h = cv2.boundingRect(bird_contours[0])
    else:
        bird_x, bird_y, bird_w, bird_h = -1, -1, -1, -1

    # 找到管道的位置信息
    pipe_contours, _ = cv2.findContours(mask_pipe, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pipe_positions = []
    for contour in pipe_contours:
        x, y, w, h = cv2.boundingRect(contour)
        pipe_positions.append((x, y, w, h))

    # 返回提取的状态信息
    return bird_x, bird_y, bird_w, bird_h, pipe_positions


'''
action 
'''
def act (driver):
    driver.find_element_by_id("element_id").send_keys(Keys.SPACE);
