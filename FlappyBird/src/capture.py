# 截取游戏画面
import numpy as np
from utils import get_game_window
import cv2


def capture(driver):
    game_window = get_game_window(driver)
    # 获取游戏窗口的位置和大小信息
    location = game_window.location
    size = game_window.size
    print('location{}, size{}', location, size)
    # 获取游戏窗口的截图
    screenshot = driver.get_screenshot_as_png()
    # save_screenshot(screenshot, 'screenshot')

    # 将二进制数据转换成 OpenCV 图像格式
    nparr = np.frombuffer(screenshot, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 截取游戏窗口的图像
    game_frame = img_np[location['y']:location['y'] + size['height'], location['x']:location['x'] + size['width']]
    # 保存截取的图像
    # output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "game_frame.png")
    # cv2.imwrite(output_path, game_frame)

    # 创建窗口并设置大小
    cv2.namedWindow('GAME', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('GAME', size['width'], size['height'])

    return game_frame
