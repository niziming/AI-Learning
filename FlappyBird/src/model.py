# AI 模型的定义.py
import cv2

from FlappyBird.src.utils import extract_game_state


class FlappyBirdAgent:
    def __init__(self):
        pass

    def decide_action(self, bird_y, pipe_positions):
        # 默认动作为不跳跃
        action = "NOOP"

        # 判断小鸟是否在管道的高度范围内
        for x, y, w, h in pipe_positions:
            if bird_y > y and bird_y < y + h:
                # 小鸟在管道的高度范围内，判断是否需要跳跃
                if x + w < 50:  # 管道即将出现在小鸟前方，需要跳跃
                    action = "JUMP"
                    break

        return action

# 使用示例
agent = FlappyBirdAgent()

# 假设提取的游戏状态信息为：
game_screen = cv2.imread('../resources/game_frame1.png')
bird_x, bird_y, bird_w, bird_h, pipe_positions = extract_game_state(game_screen)
print(bird_x, bird_y, bird_w, bird_h, pipe_positions)

# 根据游戏状态信息做出决策
action = agent.decide_action(bird_y, pipe_positions)
print("Action:", action)

# 绘制小鸟位置
cv2.rectangle(game_screen, (bird_x, bird_y), (bird_x + bird_w, bird_y + bird_h), (0, 255, 0), 4)

# 绘制管道位置
for pipe in pipe_positions:
    x, y, w, h = pipe
    cv2.rectangle(game_screen, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 显示检测结果
cv2.imshow('Detection Result', game_screen)
cv2.waitKey(0)
