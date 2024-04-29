# 截取游戏画面的脚本
import webbrowser
from selenium import webdriver
from utils import get_webdriver
import cv2

# 输入网址
# url = input("Enter your web url: ")
url = "https://zh.y8.com/games/flappy_bird_"




# 获取 WebDriver 实例并访问网页
driver = get_webdriver(url)

# 等待游戏加载完成
driver.implicitly_wait(5)

# 获取游戏窗口的位置和大小
game_window = driver.find_element_by_class_name('flappy bird')

# 获取游戏窗口的位置和大小信息
location = game_window.location
size = game_window.size

# 获取游戏窗口的截图
screenshot = driver.get_screenshot_as_png()

# 将二进制数据转换成 OpenCV 图像格式
nparr = np.frombuffer(screenshot, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# 截取游戏窗口的图像
game_frame = img_np[location['y']:location['y'] + size['height'], location['x']:location['x'] + size['width']]

# 显示截取的图像
cv2.imshow('Game Frame', game_frame)
cv2.waitKey(0)

# 关闭浏览器
driver.quit()
