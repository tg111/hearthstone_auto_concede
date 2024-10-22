import time
import tools
import restart_hs

# 重试次数
retry_count = 0
# 最大重试次数
max_retry_count = 180


# 主页
def main_menu():
    main_menu_button = tools.match_template('image/main_menu.png')
    if main_menu_button:
        reset_retry_count()
        print('主页，进入传统对战')
        tools.click(main_menu_button[0] + 10, main_menu_button[1] + 10)  # 点击开始游戏按钮
        time.sleep(2)


# 准备阶段：点击开始游戏按钮
def start_game():
    start_button = tools.match_template('image/start_game_button.png')
    if start_button:
        reset_retry_count()
        print("开始匹配")
        tools.click(start_button[0] + 10, start_button[1] + 10)  # 点击开始游戏按钮
        time.sleep(2)


# 匹配中阶段：如果看到排队字样，取消匹配并返回准备阶段
def cancel_queue():
    cancel_button = tools.match_template('image/cancel_button.png')  # 取消按钮
    if cancel_button:
        reset_retry_count()
        print("匹配中...")
        # 识别"排队"字样的图片
        queue_sign = tools.match_template('image/queue_sign.png')
        if queue_sign:
            print("检测到排队计时，取消匹配")
            cancel_button = tools.match_template('image/cancel_button.png')  # 匹配“取消”按钮
            if cancel_button:
                tools.click(cancel_button[0] + 10, cancel_button[1] + 10)  # 点击取消按钮
                time.sleep(2)


# 选牌阶段：按ESC并点击投降
def concede_game():
    confirm_button = tools.match_template('image/confirm_button.png')
    start_v = tools.match_template('image/start_v.png')
    if confirm_button or start_v:
        reset_retry_count()
        print("选牌阶段，执行投降")
        # 重试5次投降操作
        for i in range(0, 5):
            tools.press_key('esc')  # 按下ESC
            time.sleep(0.5)
            # 检测esc是否点早了
            surrender_none_button = tools.match_template('image/surrender_none_button.png')
            if surrender_none_button:
                print('esc点早了，重置')
                tools.press_key('esc')
                time.sleep(0.5)
                continue
            surrender_button = tools.match_template('image/surrender_button.png')
            if surrender_button:
                tools.click(surrender_button[0] + 10, surrender_button[1] + 10)  # 点击投降按钮
                time.sleep(2)
            break


# 投降结束阶段：点击失败两个字
def finish_game():
    shibai_sidai = tools.match_template('image/shibai_sidai.png')
    if shibai_sidai:
        reset_retry_count()
        print("结束，失败丝带，点击继续")
        tools.click(shibai_sidai[0] + 10, shibai_sidai[1] + 10)  # 点击失败的字样
        time.sleep(2)
    defeat_sign = tools.match_template('image/defeat_sign.png')
    win_sign = tools.match_template('image/win_sign.png')
    if defeat_sign or win_sign:
        reset_retry_count()
        print("结束，点击继续")
        click_btn = defeat_sign if defeat_sign else win_sign
        tools.click(click_btn[0] + 10, click_btn[1] + 10)  # 点击失败的字样
        time.sleep(2)
    sidai = tools.match_template('image/sidai.png')
    if sidai:
        reset_retry_count()
        print("结束丝带，点击继续")
        tools.click(sidai[0] + 10, sidai[1] + 10)  # 点击失败的字样
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
            print("程序{}分钟无响应，重启程序".format(str(int(max_retry_count / 60))))
            restart_hs.main()
            reset_retry_count()
            continue
        print('识别中...')
        main_menu()  # 检测是否在主页，是则进入对战选牌
        start_game()  # 检测是否在准备阶段，并点击开始游戏
        cancel_queue()  # 检测是否匹配中，是否需要取消匹配
        concede_game()  # 检测是否进入选牌阶段，并执行投降操作
        finish_game()  # 检测是否结束游戏，并点击返回准备阶段
        time.sleep(1)  # 等待一段时间后重新开始循环
        retry_count += 1


if __name__ == "__main__":
    auto_concede()
