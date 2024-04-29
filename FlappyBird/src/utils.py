# 工具函数
import datetime
import os
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
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
        driver.set_window_size(1920, 1080)  # 例如设置为1920x1080像素
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
        else:
            print("Game window found:", game_window)
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
    filename = os.path.join(project_root, "data", prefix + str(int(time.time())) + ".png")

    # 保存截图
    with open(filename, 'wb') as f:
        f.write(screenshot)

    print(filename)
    return filename