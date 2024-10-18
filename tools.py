from PIL import ImageGrab
import numpy as np
import cv2
import pyautogui


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
