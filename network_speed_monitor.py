#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时网速监控程序 —— 紧凑面板版
- 小巧半透明面板显示实时下载/上传速度
- 始终置顶，可拖拽移动
- 右键菜单退出
"""

import psutil
import tkinter as tk
import time
import sys

# ── 颜色主题 ──
BG_DARK      = '#1a1a2e'
BG_MEDIUM    = '#16213e'
ACCENT_DOWN  = '#00d2ff'   # 下载 - 青色
ACCENT_UP    = '#ff6b6b'   # 上传 - 珊瑚红
TEXT_PRIMARY = '#e0e0e0'
TEXT_SEC     = '#8899aa'
BORDER       = '#2a2a4a'


def format_speed(bps):
    """将 bytes/s 格式化为可读字符串"""
    if bps < 0:
        bps = 0
    if bps < 1024:
        return f'{bps:.1f} B/s'
    elif bps < 1024 ** 2:
        return f'{bps / 1024:.1f} KB/s'
    elif bps < 1024 ** 3:
        return f'{bps / (1024 ** 2):.2f} MB/s'
    else:
        return f'{bps / (1024 ** 3):.2f} GB/s'


class SpeedMonitor:
    """核心网速监控器"""

    def __init__(self):
        self.old_counters = psutil.net_io_counters()
        self.old_time = time.time()

    def get_speed(self):
        """获取瞬时网速 (bytes/s)，返回 (download, upload)"""
        try:
            new = psutil.net_io_counters()
            new_time = time.time()
            elapsed = new_time - self.old_time
            if elapsed <= 0:
                return (0.0, 0.0)
            dl = (new.bytes_recv - self.old_counters.bytes_recv) / elapsed
            ul = (new.bytes_sent - self.old_counters.bytes_sent) / elapsed
            self.old_counters = new
            self.old_time = new_time
            return (max(dl, 0), max(ul, 0))
        except Exception:
            return (0.0, 0.0)


class NetSpeedPanel(tk.Tk):
    """紧凑信息面板"""

    def __init__(self):
        super().__init__()
        self.title('实时网速')
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.92)
        self.configure(bg=BG_DARK)

        # ── 窗口尺寸与位置（右上角） ──
        W, H = 230, 95
        sw = self.winfo_screenwidth()
        self.geometry(f'{W}x{H}+{sw - W - 30}+50')

        # ── 拖拽状态 ──
        self._drag_data = {'x': 0, 'y': 0}

        # ── 构建界面 ──
        self._build_ui()

        # ── 启动网速监控 ──
        self.monitor = SpeedMonitor()
        self._update_speed()

    def _build_ui(self):
        # 主容器
        main = tk.Frame(self, bg=BG_DARK,
                        highlightbackground=BORDER,
                        highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True)

        # ── 标题栏（可拖拽） ──
        title_bar = tk.Frame(main, bg=BG_MEDIUM, height=26)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)

        icon = tk.Label(title_bar, text='🌐', bg=BG_MEDIUM,
                        fg=TEXT_PRIMARY, font=('Segoe UI', 10))
        icon.pack(side=tk.LEFT, padx=(8, 4))

        title_lbl = tk.Label(title_bar, text='实时网速', bg=BG_MEDIUM,
                             fg=TEXT_SEC, font=('微软雅黑', 9))
        title_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        close_btn = tk.Label(title_bar, text='✕', bg=BG_MEDIUM,
                             fg=TEXT_SEC, font=('Arial', 11, 'bold'),
                             cursor='hand2')
        close_btn.pack(side=tk.RIGHT, padx=(0, 8))
        close_btn.bind('<Button-1>', lambda e: self.quit_app())

        # 绑定拖拽事件到标题栏区域
        for w in (title_bar, icon, title_lbl):
            w.bind('<Button-1>', self._drag_start)
            w.bind('<B1-Motion>', self._drag_move)

        # ── 速度显示 ──
        body = tk.Frame(main, bg=BG_DARK)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=(6, 8))

        # 下载行
        dl_row = tk.Frame(body, bg=BG_DARK)
        dl_row.pack(fill=tk.X, pady=(3, 1))

        tk.Label(dl_row, text='⬇', bg=BG_DARK,
                 fg=ACCENT_DOWN, font=('Arial', 12)).pack(side=tk.LEFT)
        tk.Label(dl_row, text='下载', bg=BG_DARK,
                 fg=TEXT_SEC, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=(5, 0))

        self.dl_val = tk.Label(dl_row, text='0.0 KB/s', bg=BG_DARK,
                               fg=ACCENT_DOWN,
                               font=('Consolas', 10, 'bold'))
        self.dl_val.pack(side=tk.RIGHT)

        # 上传行
        ul_row = tk.Frame(body, bg=BG_DARK)
        ul_row.pack(fill=tk.X, pady=(1, 3))

        tk.Label(ul_row, text='⬆', bg=BG_DARK,
                 fg=ACCENT_UP, font=('Arial', 12)).pack(side=tk.LEFT)
        tk.Label(ul_row, text='上传', bg=BG_DARK,
                 fg=TEXT_SEC, font=('微软雅黑', 9)).pack(side=tk.LEFT, padx=(5, 0))

        self.ul_val = tk.Label(ul_row, text='0.0 KB/s', bg=BG_DARK,
                               fg=ACCENT_UP,
                               font=('Consolas', 10, 'bold'))
        self.ul_val.pack(side=tk.RIGHT)

        # ── 右键菜单 ──
        menu = tk.Menu(self, tearoff=0, bg=BG_MEDIUM,
                       fg=TEXT_PRIMARY,
                       activebackground='#0f3460',
                       activeforeground=TEXT_PRIMARY)
        menu.add_command(label='退出', command=self.quit_app)
        self.bind('<Button-3>', lambda e: menu.tk_popup(e.x_root, e.y_root))

    # ── 拖拽 ──
    def _drag_start(self, event):
        self._drag_data['x'] = event.x
        self._drag_data['y'] = event.y

    def _drag_move(self, event):
        x = self.winfo_x() + event.x - self._drag_data['x']
        y = self.winfo_y() + event.y - self._drag_data['y']
        self.geometry(f'+{x}+{y}')

    # ── 速度更新 ──
    def _update_speed(self):
        dl, ul = self.monitor.get_speed()
        self.dl_val.config(text=format_speed(dl))
        self.ul_val.config(text=format_speed(ul))
        self.after(1000, self._update_speed)

    def quit_app(self):
        self.destroy()
        sys.exit(0)


if __name__ == '__main__':
    app = NetSpeedPanel()
    app.mainloop()