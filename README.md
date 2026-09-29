# 实时网速监控悬浮窗

一个轻量级的 Windows 桌面工具，在屏幕右上角显示实时网络下载/上传速度。

## 特点

- ⚡ **实时监控** —— 每秒刷新，显示下载与上传速度
- 🎨 **简洁美观** —— 深色半透明面板，适配 Windows 现代风格
- 📌 **始终置顶** —— 不会被其他窗口遮挡，随时查看
- 🖱️ **可拖拽** —— 鼠标拖拽标题栏任意移动位置
- 📏 **自动单位** —— B/s, KB/s, MB/s, GB/s 自动适配
- 🚫 **零依赖** —— 提供独立 exe，无需安装 Python 环境

## 使用方式

### 方式一：直接运行 exe

从 [Releases](https://github.com/SCLyu4462/NetSpeedPanel/releases) 页面下载最新版 `NetSpeedMonitor.exe`，双击即可启动。

### 方式二：Python 源码运行

```bash
pip install psutil
python network_speed_monitor.py
```

### 方式三：批处理脚本

双击 `start_net_speed.bat`。

### 操作

| 操作 | 效果 |
|------|------|
| 鼠标左键拖拽标题栏 | 移动位置 |
| 鼠标右键点击面板 | 退出程序 |

## 文件结构

```
├── network_speed_monitor.py  # Python 源码
├── start_net_speed.bat       # 快捷启动脚本
├── .gitignore
├── LICENSE
└── README.md
```

> 独立 exe（免安装）请从 [Releases](https://github.com/SCLyu4462/NetSpeedPanel/releases) 下载，不再随仓库分发。

## 技术栈

- Python 3.13
- [psutil](https://github.com/giampaolo/psutil) —— 获取网络流量数据
- tkinter —— 原生 GUI 界面
- PyInstaller —— 打包为独立 exe