# 主程序入口
from selenium.webdriver import ActionChains, Keys
from FlappyBird.src.DQNAgent import DQNAgent
from capture import capture
from utils import *


# 定义鼠标事件回调函数
def get_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button of the mouse is clicked - position (", x, ", ", y, ")")
        action.move_to_element_with_offset(game_window, x, y).click().perform()
        return x, y


# 输入网址
url = "https://flappybird.io/"

# 获取 WebDriver 实例并访问网页
driver = get_webdriver(url)

# 获取游戏窗口的位置和大小
game_window = get_game_window(driver)

action = ActionChains(driver)

# 强化学习的初始化
state_height, state_width = 480, 640  # 假设游戏画面是 480*640 的像素图像
state_channels = 3  # 假设游戏画面是 RGB 彩色图像
# 根据你的游戏动作定义
action_size = 2  # 假设有两种动作：跳跃和不跳跃
# 根据你的游戏状态定义
state_size = state_height * state_width * state_channels

agent = DQNAgent(state_size, action_size)

# 执行动作
def perform_action(action_id):
    if action_id == 0:
        # 如果动作是 0，则执行跳跃动作
        action.send_keys()
        action.send_keys(Keys.SPACE).perform()
    else:
        # 如果动作是其他值，则不执行任何动作，让游戏按照自己的物理规则进行下落
        pass

# 是否碰撞
def check_bird_hit_pipe(bird_x, bird_y, bird_w, bird_h, pipe_positions):
    for pipe in pipe_positions:
        pipe_x, pipe_y, pipe_w, pipe_h = pipe
        # 判断小鸟和管道是否发生碰撞
        if (bird_x < pipe_x + pipe_w and
                bird_x + bird_w > pipe_x and
                bird_y < pipe_y + pipe_h and
                bird_y + bird_h > pipe_y):
            print("小鸟碰撞了管道")
            return True  # 小鸟碰撞了管道
    print("小鸟没有碰撞管道")
    return False  # 小鸟没有碰撞管道


# 是否撞到管道
def bird_hit_pipe(bird_x, bird_y, bird_w, bird_h, pipe_positions):
    # 遍历所有管道，检查小鸟是否与管道碰撞
    for pipe in pipe_positions:
        pipe_x, pipe_y, pipe_w, pipe_h = pipe
        if (bird_x < pipe_x + pipe_w and
                bird_x + bird_w > pipe_x and
                bird_y < pipe_y + pipe_h and
                bird_y + bird_h > pipe_y):
            print("小鸟碰撞了管道")
            return True  # 小鸟碰撞了管道
    print("小鸟碰撞了管道")
    return False  # 小鸟没有碰撞管道


# 是否掉出屏幕外
def check_bird_fall_out_of_screen(bird_x, bird_y, bird_w, bird_h, pipe_positions, game_frame):
    # 获取小鸟的位置信息
    screen_height = game_frame.shape[0]  # 屏幕的高度

    # 如果小鸟的纵坐标超出了屏幕范围，则认为小鸟掉出了屏幕外
    if bird_y + bird_h > screen_height:
        print("小鸟掉出了屏幕外")
        return True  # 小鸟掉出了屏幕外
    else:
        print("小鸟没有掉出屏幕外")
        return False  # 小鸟没有掉出屏幕外


# 计算奖励
def calculate_reward(bird_y, bird_h, next_bird_y, next_bird_h, bird_hit_pipe):
    # 如果小鸟向上移动了，给予正奖励
    if next_bird_y < bird_y:
        print("如果小鸟向上移动了，给予正奖励")
        reward = 1
    # 如果小鸟向下移动了或者碰到了管道，给予负奖励
    elif next_bird_y > bird_y or bird_hit_pipe:
        print("如果小鸟向上移动了，给予正奖励")
        reward = -1
    # 如果小鸟保持不动，给予小的负奖励
    else:
        print("如果小鸟保持不动，给予小的负奖励")
        reward = -0.1
    return reward


# 是否结束
def check_game_over(bird_x, bird_y, bird_w, bird_h, pipe_positions, game_frame):
    # 根据游戏画面判断游戏是否结束，这里简单地假设游戏结束的条件是小鸟碰撞管道或者掉到屏幕底部
    bird_hit_pipe = check_bird_hit_pipe(bird_x, bird_y, bird_w, bird_h, pipe_positions)
    bird_fall_out_of_screen = check_bird_fall_out_of_screen(bird_x, bird_y, bird_w, bird_h, pipe_positions, game_frame)
    if bird_hit_pipe or bird_fall_out_of_screen:
        return True  # 游戏结束
    else:
        return False  # 游戏未结束


# 循环进行以下操作：
while True:
    # 1获取游戏窗口的截图。
    game_frame = capture(driver)

    # 2提取游戏状态信息。
    bird_x, bird_y, bird_w, bird_h, pipe_positions = extract_game_state(game_frame)
    bird_hit_pipe = check_bird_hit_pipe(bird_x, bird_y, bird_w, bird_h, pipe_positions)

    # 绘制小鸟位置
    cv2.rectangle(game_frame, (bird_x, bird_y), (bird_x + bird_w, bird_y + bird_h), (0, 255, 0), 4)

    # 绘制管道位置
    for pipe in pipe_positions:
        x, y, w, h = pipe
        cv2.rectangle(game_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 使用强化学习的神经网络模型预测动作。
    action_id = agent.select_action(game_frame)  # 选择动作
    perform_action(action_id)  # 执行动作

    # 获取游戏状态
    next_game_frame = capture(driver)
    next_bird_x, next_bird_y, next_bird_w, next_bird_h, next_pipe_positions = extract_game_state(next_game_frame)

    reward = calculate_reward(bird_x, bird_y, next_bird_x, next_bird_y, bird_hit_pipe)  # 计算奖励
    done = check_game_over(bird_x, bird_y, bird_w, bird_h, pipe_positions, game_frame)  # 检查游戏是否结束
    print("done{}", done)
    # 存储经验并训练模型
    agent.store_experience(game_frame, action_id, reward, next_game_frame, done)
    agent.train(done)  # 执行动作

    # 显示检测结果
    cv2.imshow('GAME', game_frame)
    # 等待键盘输入，参数表示每次等待键盘输入的毫秒数
    key = cv2.waitKey(20)

    # region 人工干预部分
    # 如果按下 ESC 键或窗口关闭按钮，则退出循环
    if key == 27 or key == ord('q'):
        break
    # 如果按下空格键（ASCII 值为 32），则执行某些操作
    elif key == 32:
        print("Space bar pressed!")
        # 在这里执行空格键被按下时的操作 同事点击浏览器的空格
        # 替换为
        action.send_keys(Keys.SPACE).perform()
    # 如果按下左键
    # cv2.setMouseCallback("Result", get_mouse_click)
    # endregion

# 关闭 OpenCV 窗口
cv2.destroyAllWindows()
# 关闭浏览器
driver.quit()
