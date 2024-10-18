import pygetwindow as gw
import time
import tools
import psutil


# 根据进程名称杀死战网进程
def kill_process_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            print(f"正在终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.terminate()  # 尝试优雅终止进程
            proc.wait(timeout=5)  # 等待最多5秒确认进程已终止
            if proc.is_running():
                print(f"无法优雅终止，强制终止 {proc.info['name']}")
                proc.kill()  # 如果无法优雅终止，则强制终止
            print(f"进程 {proc.info['name']} 已终止")
            time.sleep(3)
            return True
    return False


def activate_window(windowTitle):
    windows = gw.getWindowsWithTitle(windowTitle)
    if windows:
        window = windows[0]
        window.restore()
        time.sleep(2)


def start_game_from_battle_net():
    hs_icon = tools.match_template('image/hs_icon.png')
    if hs_icon:
        tools.click(hs_icon[0] + 10, hs_icon[1] + 10)  # 切换到炉石tab
    start_button = tools.match_template('image/start_hs_button.png')
    if start_button:
        tools.click(start_button[0] + 10, start_button[1] + 10)  # 点击启动游戏按钮
        time.sleep(2)
    else:
        print("未找到启动按钮")
        exit()


def main():
    # 杀死进程
    kill_process_by_name('Hearthstone')
    # 激活战网窗口
    activate_window('战网')
    # 开始游戏
    start_game_from_battle_net()


if __name__ == '__main__':
    main()
