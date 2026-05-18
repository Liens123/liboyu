"""桌面宠物 - 主程序入口"""

import tkinter as tk
import sys
import time

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    FPS, AUTO_SAVE_INTERVAL, STATE_IDLE,
)
from pet import Pet
from renderer import draw_cat, draw_bubble, draw_status_indicator, draw_skill_effect
from ui import StatusPanel, ContextMenu
from persistence import save_game, load_game


class DesktopPetApp:
    """桌面宠物主应用"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("桌面宠物")

        # 窗口设置：无边框、透明、置顶
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#f0f0f0")
        self.root.config(bg="#f0f0f0")

        # 窗口大小
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # 创建 Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg="#f0f0f0",
            highlightthickness=0,
        )
        self.canvas.pack()

        # 加载或创建宠物
        saved_pet, saved_pos = load_game()
        if saved_pet:
            self.pet = saved_pet
        else:
            self.pet = Pet("小猫咪")

        # 窗口位置
        if saved_pos:
            self.root.geometry(f"+{saved_pos[0]}+{saved_pos[1]}")
        else:
            # 屏幕右下角
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            self.root.geometry(f"+{screen_w - WINDOW_WIDTH - 50}+{screen_h - WINDOW_HEIGHT - 100}")

        # UI 组件
        self.status_panel = StatusPanel(self.root, self.pet)
        self.context_menu = ContextMenu(self.root, self.pet, self._on_action)

        # 名称标签（放在底部）
        self.name_label = tk.Label(
            self.root,
            text=f"{self.pet.name} Lv.{self.pet.level}",
            font=("Microsoft YaHei", 9, "bold"),
            fg="#555", bg="#f0f0f0",
        )
        self.name_label.place(x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT - 15, anchor="center")

        # 绑定事件
        self._bind_events()

        # 动画状态
        self.anim_tick = 0
        self.last_save_time = 0

        # 启动主循环
        self._update_loop()

    def _bind_events(self):
        """绑定鼠标事件"""
        # 拖拽
        self.canvas.bind("<Button-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self._on_drag_end)

        # 右键菜单
        self.canvas.bind("<Button-3>", self.context_menu.show)

        # 双击打开状态面板
        self.canvas.bind("<Double-Button-1>", lambda e: self.status_panel.show())

    def _on_drag_start(self, event):
        """开始拖拽"""
        self._drag_x = event.x
        self._drag_y = event.y
        self._dragging = True

    def _on_drag_motion(self, event):
        """拖拽中"""
        if hasattr(self, '_dragging') and self._dragging:
            dx = event.x - self._drag_x
            dy = event.y - self._drag_y
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")

    def _on_drag_end(self, event):
        """结束拖拽"""
        self._dragging = False

    def _on_action(self, action):
        """处理右键菜单操作"""
        if action == "feed":
            self.pet.feed()
        elif action == "play":
            self.pet.play()
        elif action == "clean":
            self.pet.clean()
        elif action == "heal":
            self.pet.heal()
        elif action == "status":
            self.status_panel.show()
        elif action == "save":
            self._save_game()
        elif action == "quit":
            self._save_game()
            self.root.destroy()
            sys.exit()
        elif action.startswith("skill:"):
            idx = int(action.split(":")[1])
            self.pet.perform_skill(idx)

    def _update_loop(self):
        """主更新循环"""
        # 更新宠物状态
        self.pet.update()

        # 更新名称标签
        self.name_label.config(text=f"{self.pet.name} Lv.{self.pet.level}")

        # 确定当前状态
        if self.pet.performing_skill:
            current_state = "skill"
        else:
            current_state = self.pet.state

        # 绘制猫咪
        draw_cat(self.canvas, current_state, self.anim_tick)

        # 绘制气泡
        if self.pet.bubble_visible:
            draw_bubble(
                self.canvas,
                self.pet.bubble_text,
                WINDOW_WIDTH / 2,
                WINDOW_HEIGHT / 2 - 20,
            )
        else:
            self.canvas.delete("bubble")

        # 绘制状态指示器
        if self.pet.state not in (STATE_IDLE, STATE_HAPPY):
            draw_status_indicator(self.canvas, self.pet.state, WINDOW_WIDTH - 25, 20)

        # 技能特效
        if self.pet.performing_skill:
            draw_skill_effect(
                self.canvas,
                self.pet.current_skill.get("name") if self.pet.current_skill else None,
                WINDOW_WIDTH / 2,
                WINDOW_HEIGHT / 2 - 20,
                self.anim_tick,
            )
        else:
            self.canvas.delete("skill_effect")

        # 更新状态面板
        self.status_panel.update()

        # 自动保存
        now = time.time()
        if now - self.last_save_time >= AUTO_SAVE_INTERVAL:
            self._save_game()
            self.last_save_time = now

        # 下一帧
        self.anim_tick += 1
        interval = int(1000 / FPS)
        self.root.after(interval, self._update_loop)

    def _save_game(self):
        """保存游戏"""
        pos = (self.root.winfo_x(), self.root.winfo_y())
        save_game(self.pet, pos)

    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """程序入口"""
    app = DesktopPetApp()
    app.run()


if __name__ == "__main__":
    main()
