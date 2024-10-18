# 炉石传说自动投降脚本

## 项目简介
本项目是一个用于《炉石传说》的自动化投降脚本，通过图像识别和模拟鼠标点击实现自动开始游戏并投降的功能。脚本会循环执行以下几个阶段：
1. **准备阶段**：识别到“开始游戏”按钮后，点击进入匹配阶段。
2. **匹配中阶段**：识别到“排队”字样后，点击取消匹配并返回准备阶段。
3. **选牌阶段**：进入选牌界面后，按下ESC并自动点击投降按钮。
4. **投降结束阶段**：识别到失败字样后，点击屏幕以返回准备阶段，重新开始循环。

## 环境配置

### 所需库
- `pyautogui`: 用于模拟鼠标点击和键盘操作
- `opencv-python`: 用于图像识别
- `pillow`: 用于截图
- `numpy`: 用于处理图像数据

### 安装步骤
使用以下命令安装所需库：
```bash
pip install pyautogui opencv-python pillow numpy psutil
```
### 免责声明

本脚本仅供学习和技术交流使用，任何因使用本脚本导致的《炉石传说》账号被封、损失等后果，作者不承担任何责任。请谨慎使用，切勿滥用本脚本进行违规操作。

> 使用本脚本即表示您已接受上述免责声明。

### 注意事项

- 作者分辨率为1920x1080窗口化，其他分辨率可能需要重新截图。
- 请确保截取的按钮或字样图片准确清晰，以保证脚本的识别率。
- 不同设备和游戏分辨率下，图像识别的效果可能有所差异，请根据实际情况调整截图和匹配阈值。
- 使用该脚本可能违反游戏的服务条款，存在封号风险。请自行承担相关风险。

### 待办事项

- [ ] 集成OCR文字识别功能，用于识别“失败”字样，进一步提升流程速度
- [x] 优化进入游戏后快速投降的逻辑，缩短响应时间
- [ ] 增加点击位置的随机偏移值，避免每次点击同一位置被检测到，提升安全性
- [x] 游戏崩溃、无响应后重启游戏
