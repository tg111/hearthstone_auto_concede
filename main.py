import pyautogui
import cv2
import time
from PIL import ImageGrab
import numpy as np

# 重试次数
retry_count = 0
# 最大重试次数
max_retry_count = 300


# 模板匹配函数，用于识别屏幕上某个阶段的图像
def match_template(template_path, threshold=0.9):
    # 截取当前屏幕并转换为numpy数组
    screen = np.array(ImageGrab.grab())
    # 读取模板图片
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, 0)
    try:
        # 使用cv2.matchTemplate进行模板匹配
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    except cv2.error:
        return None
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return max_loc  # 返回匹配位置
    else:
        return None


# 点击给定的坐标
def click(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()


# 模拟按键
def press_key(key):
    pyautogui.press(key)


# 准备阶段：点击开始游戏按钮
def start_game():
    start_button = match_template('image/start_game_button.png')
    if start_button:
        reset_retry_count()
        print("开始匹配")
        click(start_button[0] + 10, start_button[1] + 10)  # 点击开始游戏按钮
        time.sleep(2)


# 匹配中阶段：如果看到排队字样，取消匹配并返回准备阶段
def cancel_queue():
    cancel_button = match_template('image/cancel_button.png')  # 取消按钮
    if cancel_button:
        reset_retry_count()
        print("匹配中...")
        # 识别"排队"字样的图片
        queue_sign = match_template('image/queue_sign.png')
        if queue_sign:
            print("检测到排队计时，取消匹配")
            cancel_button = match_template('image/cancel_button.png')  # 匹配“取消”按钮
            if cancel_button:
                click(cancel_button[0] + 10, cancel_button[1] + 10)  # 点击取消按钮
                time.sleep(2)


# 选牌阶段：按ESC并点击投降
def concede_game():
    confirm_button = match_template('image/confirm_button.png')
    if confirm_button:
        reset_retry_count()
        print("选牌阶段，执行投降")
        press_key('esc')  # 按下ESC
        time.sleep(1)
        surrender_button = match_template('image/surrender_button.png')
        if surrender_button:
            click(surrender_button[0] + 10, surrender_button[1] + 10)  # 点击投降按钮
            time.sleep(2)


# 投降结束阶段：点击失败两个字
def finish_game():
    defeat_sign = match_template('image/defeat_sign.png')
    win_sign = match_template('image/win_sign.png')
    sidai = match_template('image/sidai.png')
    if defeat_sign or win_sign:
        reset_retry_count()
        print("结束，点击继续")
        click_btn = defeat_sign if defeat_sign else win_sign
        click(click_btn[0] + 10, click_btn[1] + 10)  # 点击失败的字样
        time.sleep(2)
    if sidai:
        reset_retry_count()
        print("结束丝带，点击继续")
        click(sidai[0] + 10, sidai[1] + 10)  # 点击失败的字样
        time.sleep(2)


# 重置重试次数
def reset_retry_count():
    global retry_count
    retry_count = 0


# 自动循环过程
def auto_concede():
    global retry_count
    global max_retry_count
    while True:
        if retry_count >= max_retry_count:
            print("5分钟无响应，退出程序")
            break
        print('识别中...')
        start_game()  # 检测是否在准备阶段，并点击开始游戏
        cancel_queue()  # 检测是否匹配中，是否需要取消匹配
        concede_game()  # 检测是否进入选牌阶段，并执行投降操作
        finish_game()  # 检测是否结束游戏，并点击返回准备阶段
        time.sleep(1)  # 等待一段时间后重新开始循环
        retry_count += 1


if __name__ == "__main__":
    auto_concede()
