"""桌面宠物 - 界面组件"""

import tkinter as tk
from tkinter import ttk
from config import (
    STATE_IDLE, STATE_HAPPY, STATE_HUNGRY, STATE_SLEEPY, STATE_DIRTY, STATE_SICK,
    MAX_STAT, SKILLS,
)


class StatusPanel:
    """宠物状态面板"""

    def __init__(self, parent, pet):
        self.parent = parent
        self.pet = pet
        self.window = None
        self.bars = {}

    def show(self):
        """显示状态面板"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{self.pet.name} - 状态")
        self.window.geometry("280x420")
        self.window.resizable(False, False)
        self.window.configure(bg="#f5f5f5")

        # 使面板跟随主窗口
        self.window.transient(self.parent)

        self._build_ui()
        self.update()

    def _build_ui(self):
        """构建界面"""
        pet = self.pet
        bg = "#f5f5f5"

        # 标题
        title_frame = tk.Frame(self.window, bg="#4CAF50", pady=8)
        title_frame.pack(fill="x")
        tk.Label(
            title_frame, text=f"🐱 {pet.name}",
            font=("Microsoft YaHei", 14, "bold"),
            fg="white", bg="#4CAF50"
        ).pack()

        # 基本信息
        info_frame = tk.Frame(self.window, bg=bg, pady=8, padx=16)
        info_frame.pack(fill="x")

        stage_label = tk.Label(
            info_frame,
            text=f"成长阶段: {pet.stage_info['name']}  |  等级: Lv.{pet.level}",
            font=("Microsoft YaHei", 11),
            fg="#333", bg=bg
        )
        stage_label.pack(anchor="w")
        self.stage_label = stage_label

        # 经验条
        exp_frame = tk.Frame(info_frame, bg=bg)
        exp_frame.pack(fill="x", pady=(4, 0))
        tk.Label(exp_frame, text="经验值", font=("Microsoft YaHei", 9), fg="#666", bg=bg).pack(side="left")
        exp_bar = ttk.Progressbar(exp_frame, length=180, mode="determinate")
        exp_bar.pack(side="right")
        self.bars["exp"] = exp_bar

        # 属性条
        stats_frame = tk.Frame(self.window, bg=bg, padx=16, pady=8)
        stats_frame.pack(fill="both", expand=True)

        attributes = [
            ("饥饿值", "hunger", "#FF9800"),
            ("心情值", "mood", "#E91E63"),
            ("清洁值", "cleanliness", "#2196F3"),
            ("健康值", "health", "#4CAF50"),
        ]

        for name, attr, color in attributes:
            self._create_stat_bar(stats_frame, name, attr, color)

        # 技能列表
        skills_frame = tk.Frame(self.window, bg=bg, padx=16, pady=8)
        skills_frame.pack(fill="x")

        tk.Label(
            skills_frame, text="已学技能:",
            font=("Microsoft YaHei", 10, "bold"), fg="#333", bg=bg
        ).pack(anchor="w")

        if pet.skills:
            for skill in pet.skills:
                tk.Label(
                    skills_frame,
                    text=f"  {skill['icon']} {skill['name']}",
                    font=("Microsoft YaHei", 9), fg="#555", bg=bg
                ).pack(anchor="w")
        else:
            tk.Label(
                skills_frame, text="  还没学会任何技能",
                font=("Microsoft YaHei", 9), fg="#999", bg=bg
            ).pack(anchor="w")

    def _create_stat_bar(self, parent, name, attr, color):
        """创建一个属性条"""
        frame = tk.Frame(parent, bg="#f5f5f5")
        frame.pack(fill="x", pady=4)

        tk.Label(
            frame, text=name,
            font=("Microsoft YaHei", 10), fg="#333", bg="#f5f5f5",
            width=8, anchor="w"
        ).pack(side="left")

        bar_bg = tk.Frame(frame, bg="#ddd", height=16, width=160)
        bar_bg.pack(side="left", padx=(4, 8))
        bar_bg.pack_propagate(False)

        bar_fill = tk.Frame(bar_bg, bg=color, height=16)
        bar_fill.place(x=0, y=0, relheight=1.0)

        value_label = tk.Label(
            frame, text="0",
            font=("Microsoft YaHei", 9), fg="#666", bg="#f5f5f5",
            width=4
        )
        value_label.pack(side="right")

        self.bars[attr] = (bar_fill, bar_bg, value_label)

    def update(self):
        """更新面板显示"""
        if not self.window or not self.window.winfo_exists():
            return

        pet = self.pet

        # 更新阶段标签
        self.stage_label.config(
            text=f"成长阶段: {pet.stage_info['name']}  |  等级: Lv.{pet.level}"
        )

        # 更新经验条
        self.bars["exp"]["value"] = pet.exp_progress * 100

        # 更新属性条
        for attr in ["hunger", "mood", "cleanliness", "health"]:
            if attr in self.bars:
                bar_fill, bar_bg, value_label = self.bars[attr]
                value = getattr(pet, attr)
                ratio = value / MAX_STAT
                bar_bg.update_idletasks()
                bg_width = bar_bg.winfo_width()
                if bg_width > 1:
                    bar_fill.place(x=0, y=0, width=int(bg_width * ratio), relheight=1.0)
                value_label.config(text=str(int(value)))

        # 更新技能列表
        self.window.after(1000, self.update)

    def destroy(self):
        """销毁面板"""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            self.window = None


class ContextMenu:
    """右键菜单"""

    def __init__(self, parent, pet, on_action=None):
        self.parent = parent
        self.pet = pet
        self.on_action = on_action
        self.menu = None

    def show(self, event):
        """显示右键菜单"""
        self.menu = tk.Menu(self.parent, tearoff=0, font=("Microsoft YaHei", 10))

        # 互动操作
        self.menu.add_command(label="🍖 喂食", command=lambda: self._action("feed"))
        self.menu.add_command(label="🎾 玩耍", command=lambda: self._action("play"))
        self.menu.add_command(label="🛁 清洁", command=lambda: self._action("clean"))
        self.menu.add_command(label="💊 治疗", command=lambda: self._action("heal"))

        self.menu.add_separator()

        # 技能子菜单
        if self.pet.skills:
            skill_menu = tk.Menu(self.menu, tearoff=0, font=("Microsoft YaHei", 10))
            for i, skill in enumerate(self.pet.skills):
                skill_menu.add_command(
                    label=f"{skill['icon']} {skill['name']}",
                    command=lambda idx=i: self._action(f"skill:{idx}")
                )
            self.menu.add_cascade(label="🎭 技能表演", menu=skill_menu)
        else:
            self.menu.add_command(label="🎭 技能表演 (未解锁)", state="disabled")

        self.menu.add_separator()

        # 其他
        self.menu.add_command(label="📊 查看状态", command=lambda: self._action("status"))
        self.menu.add_command(label="💾 保存", command=lambda: self._action("save"))
        self.menu.add_separator()
        self.menu.add_command(label="❌ 退出", command=lambda: self._action("quit"))

        self.menu.post(event.x_root, event.y_root)

    def _action(self, action):
        """触发操作回调"""
        if self.on_action:
            self.on_action(action)


def create_tooltip(widget, text):
    """为组件创建工具提示"""
    tooltip = None

    def show(event):
        nonlocal tooltip
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = tk.Label(
            tooltip, text=text,
            font=("Microsoft YaHei", 9),
            bg="#ffffe0", fg="#333",
            relief="solid", borderwidth=1,
            padx=4, pady=2
        )
        label.pack()

    def hide(event):
        nonlocal tooltip
        if tooltip:
            tooltip.destroy()
            tooltip = None

    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)
