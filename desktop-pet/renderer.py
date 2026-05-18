"""桌面宠物 - 矢量渲染器（用 Canvas 形状绘制，更美观）"""

import tkinter as tk
import math
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    STATE_IDLE, STATE_HAPPY, STATE_HUNGRY, STATE_SLEEPY, STATE_DIRTY, STATE_SICK,
)

# 猫咪颜色方案
CAT_COLORS = {
    "body":      "#FF8C42",   # 橘猫主色
    "body_dark": "#E07030",   # 深橘
    "belly":     "#FFD4A8",   # 肚子浅色
    "ear_outer": "#FF8C42",   # 耳朵外侧
    "ear_inner": "#FFB0B0",   # 耳朵内侧粉
    "eye_white": "#FFFFFF",   # 眼白
    "eye_pupil": "#2C2C2C",   # 瞳孔
    "eye_shine": "#FFFFFF",   # 眼睛高光
    "nose":      "#FF6B8A",   # 鼻子粉
    "mouth":     "#CC4455",   # 嘴巴
    "whisker":   "#888888",   # 胡须
    "outline":   "#3D2B1F",   # 轮廓深色
    "cheek":     "#FF9999",   # 腮红
    "tail":      "#FF8C42",   # 尾巴
    "paw":       "#FFD4A8",   # 爪子
}


def _draw_cat_body(cx, cy, scale=1.0):
    """绘制猫咪身体各部分，返回 Canvas 绘制指令列表"""
    s = scale
    parts = []

    # 尾巴（在身体后面）
    parts.append(("oval", cx - 55*s, cy + 15*s, cx - 35*s, cy + 65*s,
                  CAT_COLORS["tail"], CAT_COLORS["outline"], 2))

    # 身体（椭圆）
    parts.append(("oval", cx - 30*s, cy + 5*s, cx + 30*s, cy + 55*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 2))

    # 肚子
    parts.append(("oval", cx - 18*s, cy + 15*s, cx + 18*s, cy + 48*s,
                  CAT_COLORS["belly"], "", 0))

    # 左耳（三角形）
    ear_l = [
        (cx - 28*s, cy - 15*s),
        (cx - 38*s, cy - 50*s),
        (cx - 8*s, cy - 25*s),
    ]
    parts.append(("polygon", ear_l, CAT_COLORS["ear_outer"], CAT_COLORS["outline"], 2))

    # 左耳内部
    ear_l_inner = [
        (cx - 26*s, cy - 20*s),
        (cx - 33*s, cy - 42*s),
        (cx - 13*s, cy - 27*s),
    ]
    parts.append(("polygon", ear_l_inner, CAT_COLORS["ear_inner"], "", 0))

    # 右耳（三角形）
    ear_r = [
        (cx + 28*s, cy - 15*s),
        (cx + 38*s, cy - 50*s),
        (cx + 8*s, cy - 25*s),
    ]
    parts.append(("polygon", ear_r, CAT_COLORS["ear_outer"], CAT_COLORS["outline"], 2))

    # 右耳内部
    ear_r_inner = [
        (cx + 26*s, cy - 20*s),
        (cx + 33*s, cy - 42*s),
        (cx + 13*s, cy - 27*s),
    ]
    parts.append(("polygon", ear_r_inner, CAT_COLORS["ear_inner"], "", 0))

    # 头部（圆形）
    parts.append(("oval", cx - 32*s, cy - 28*s, cx + 32*s, cy + 22*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 2))

    # 左眼白
    parts.append(("oval", cx - 22*s, cy - 15*s, cx - 6*s, cy + 5*s,
                  CAT_COLORS["eye_white"], CAT_COLORS["outline"], 1.5))

    # 左瞳孔
    parts.append(("oval", cx - 18*s, cy - 10*s, cx - 10*s, cy + 2*s,
                  CAT_COLORS["eye_pupil"], "", 0))

    # 左眼高光
    parts.append(("oval", cx - 16*s, cy - 8*s, cx - 13*s, cy - 5*s,
                  CAT_COLORS["eye_shine"], "", 0))

    # 右眼白
    parts.append(("oval", cx + 6*s, cy - 15*s, cx + 22*s, cy + 5*s,
                  CAT_COLORS["eye_white"], CAT_COLORS["outline"], 1.5))

    # 右瞳孔
    parts.append(("oval", cx + 10*s, cy - 10*s, cx + 18*s, cy + 2*s,
                  CAT_COLORS["eye_pupil"], "", 0))

    # 右眼高光
    parts.append(("oval", cx + 13*s, cy - 8*s, cx + 16*s, cy - 5*s,
                  CAT_COLORS["eye_shine"], "", 0))

    # 鼻子（小三角）
    nose_pts = [
        (cx - 4*s, cy + 5*s),
        (cx + 4*s, cy + 5*s),
        (cx, cy + 11*s),
    ]
    parts.append(("polygon", nose_pts, CAT_COLORS["nose"], "", 0))

    # 嘴巴（W 形）
    parts.append(("line", cx - 8*s, cy + 13*s, cx, cy + 17*s, CAT_COLORS["mouth"], 1.5))
    parts.append(("line", cx, cy + 17*s, cx + 8*s, cy + 13*s, CAT_COLORS["mouth"], 1.5))

    # 腮红
    parts.append(("oval", cx - 28*s, cy + 0*s, cx - 18*s, cy + 8*s,
                  CAT_COLORS["cheek"], "", 0))
    parts.append(("oval", cx + 18*s, cy + 0*s, cx + 28*s, cy + 8*s,
                  CAT_COLORS["cheek"], "", 0))

    # 左胡须
    parts.append(("line", cx - 30*s, cy + 8*s, cx - 50*s, cy + 4*s, CAT_COLORS["whisker"], 1))
    parts.append(("line", cx - 30*s, cy + 11*s, cx - 50*s, cy + 11*s, CAT_COLORS["whisker"], 1))
    parts.append(("line", cx - 30*s, cy + 14*s, cx - 50*s, cy + 18*s, CAT_COLORS["whisker"], 1))

    # 右胡须
    parts.append(("line", cx + 30*s, cy + 8*s, cx + 50*s, cy + 4*s, CAT_COLORS["whisker"], 1))
    parts.append(("line", cx + 30*s, cy + 11*s, cx + 50*s, cy + 11*s, CAT_COLORS["whisker"], 1))
    parts.append(("line", cx + 30*s, cy + 14*s, cx + 50*s, cy + 18*s, CAT_COLORS["whisker"], 1))

    # 左前腿
    parts.append(("oval", cx - 22*s, cy + 42*s, cx - 10*s, cy + 62*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 1.5))
    # 左爪子
    parts.append(("oval", cx - 20*s, cy + 56*s, cx - 12*s, cy + 63*s,
                  CAT_COLORS["paw"], CAT_COLORS["outline"], 1))

    # 右前腿
    parts.append(("oval", cx + 10*s, cy + 42*s, cx + 22*s, cy + 62*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 1.5))
    # 右爪子
    parts.append(("oval", cx + 12*s, cy + 56*s, cx + 20*s, cy + 63*s,
                  CAT_COLORS["paw"], CAT_COLORS["outline"], 1))

    return parts


def _draw_closed_eyes(canvas, cx, cy, s):
    """绘制闭眼（困倦/睡觉）"""
    # 左眼 - 弧线
    canvas.create_arc(
        cx - 22*s, cy - 15*s, cx - 6*s, cy + 5*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼 - 弧线
    canvas.create_arc(
        cx + 6*s, cy - 15*s, cx + 22*s, cy + 5*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )


def _draw_happy_eyes(canvas, cx, cy, s):
    """绘制开心眼睛（^_^ 形）"""
    # 左眼 - 弧线
    canvas.create_arc(
        cx - 22*s, cy - 15*s, cx - 6*s, cy + 5*s,
        start=180, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2.5, tags="pet"
    )
    # 右眼 - 弧线
    canvas.create_arc(
        cx + 6*s, cy - 15*s, cx + 22*s, cy + 5*s,
        start=180, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2.5, tags="pet"
    )


def _draw_sad_eyes(canvas, cx, cy, s):
    """绘制难过眼睛"""
    # 左眼 - 下垂弧线
    canvas.create_arc(
        cx - 22*s, cy - 18*s, cx - 6*s, cy + 2*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼
    canvas.create_arc(
        cx + 6*s, cy - 18*s, cx + 22*s, cy + 2*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )


def _draw_sick_face(canvas, cx, cy, s):
    """绘制生病表情（X_X）"""
    # 左眼 X
    canvas.create_line(
        cx - 20*s, cy - 12*s, cx - 8*s, cy + 0*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    canvas.create_line(
        cx - 8*s, cy - 12*s, cx - 20*s, cy + 0*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼 X
    canvas.create_line(
        cx + 8*s, cy - 12*s, cx + 20*s, cy + 0*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    canvas.create_line(
        cx + 20*s, cy - 12*s, cx + 8*s, cy + 0*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )


def draw_cat(canvas, state, frame, cx=None, cy=None):
    """在 Canvas 上绘制完整的猫咪

    Args:
        canvas: tkinter Canvas
        state: 当前状态
        frame: 动画帧号
        cx: 中心 X 坐标（默认居中）
        cy: 中心 Y 坐标（默认居中）
    """
    canvas.delete("pet")

    if cx is None:
        cx = WINDOW_WIDTH / 2
    if cy is None:
        cy = WINDOW_HEIGHT / 2 + 10

    s = 1.0  # 缩放比例

    # 呼吸动画（微微上下浮动）
    breathe_offset = math.sin(frame * 0.8) * 2
    cy += breathe_offset

    # 绘制身体各部分
    parts = _draw_cat_body(cx, cy, s)

    for part in parts:
        shape = part[0]
        if shape == "oval":
            _, x1, y1, x2, y2, fill, outline, width = part
            canvas.create_oval(x1, y1, x2, y2, fill=fill, outline=outline,
                             width=width, tags="pet")
        elif shape == "polygon":
            _, points, fill, outline, width = part
            canvas.create_polygon(points, fill=fill, outline=outline,
                                width=width, tags="pet")
        elif shape == "line":
            _, x1, y1, x2, y2, fill, width = part
            canvas.create_line(x1, y1, x2, y2, fill=fill, width=width, tags="pet")

    # 根据状态覆盖特殊表情
    if state == STATE_HAPPY:
        _draw_happy_eyes(canvas, cx, cy, s)
        # 开心嘴巴（微笑弧线）
        canvas.delete("mouth")
        canvas.create_arc(
            cx - 10*s, cy + 8*s, cx + 10*s, cy + 22*s,
            start=0, extent=-180, style="arc",
            outline=CAT_COLORS["mouth"], width=2, tags="pet"
        )
    elif state == STATE_SLEEPY:
        _draw_closed_eyes(canvas, cx, cy, s)
        # ZZZ
        if frame % 2 == 0:
            canvas.create_text(
                cx + 40*s, cy - 30*s, text="z",
                font=("Consolas", 10, "bold"), fill="#7EC8E3", tags="pet"
            )
            canvas.create_text(
                cx + 48*s, cy - 42*s, text="Z",
                font=("Consolas", 13, "bold"), fill="#7EC8E3", tags="pet"
            )
    elif state == STATE_HUNGRY:
        _draw_sad_eyes(canvas, cx, cy, s)
        # 难过嘴巴
        canvas.create_arc(
            cx - 8*s, cy + 16*s, cx + 8*s, cy + 24*s,
            start=180, extent=180, style="arc",
            outline=CAT_COLORS["mouth"], width=2, tags="pet"
        )
    elif state == STATE_SICK:
        _draw_sick_face(canvas, cx, cy, s)
        # 生病嘴巴
        canvas.create_arc(
            cx - 6*s, cy + 15*s, cx + 6*s, cy + 22*s,
            start=180, extent=180, style="arc",
            outline=CAT_COLORS["mouth"], width=1.5, tags="pet"
        )
        # 头晕星星
        if frame % 2 == 0:
            canvas.create_text(
                cx + 35*s, cy - 35*s, text="💫",
                font=("Segoe UI Emoji", 10), tags="pet"
            )
    elif state == STATE_DIRTY:
        # 脏兮兮 - 在身上画几个灰点
        import random
        random.seed(42)
        for _ in range(5):
            dx = random.randint(-20, 20)
            dy = random.randint(0, 40)
            canvas.create_oval(
                cx + dx*s - 3, cy + dy*s - 3,
                cx + dx*s + 3, cy + dy*s + 3,
                fill="#AAAAAA", outline="", tags="pet"
            )

    # 尾巴摇摆动画
    tail_swing = math.sin(frame * 1.2) * 8
    canvas.delete("tail_anim")
    # 画一个摇摆的尾巴尖
    tail_tip_x = cx - 45*s + tail_swing
    tail_tip_y = cy + 50*s + math.sin(frame * 0.6) * 5
    canvas.create_line(
        cx - 45*s, cy + 40*s, tail_tip_x, tail_tip_y,
        fill=CAT_COLORS["tail"], width=4, smooth=True, tags="pet"
    )


def draw_bubble(canvas, text, pet_cx, pet_top_y):
    """在宠物头顶绘制对话气泡"""
    canvas.delete("bubble")

    if not text:
        return

    font_size = 10
    bubble_x = pet_cx
    bubble_y = pet_top_y - 55

    # 计算文字宽度（中文字符约 14px，英文约 7px）
    text_width = 0
    for ch in text:
        if ord(ch) > 127:
            text_width += 14
        else:
            text_width += 7
    text_width = max(text_width + 20, 50)
    text_height = font_size + 14

    # 气泡背景（圆角矩形）
    x1 = bubble_x - text_width / 2
    y1 = bubble_y - text_height
    x2 = bubble_x + text_width / 2
    y2 = bubble_y
    r = 8  # 圆角半径

    # 用多个形状模拟圆角矩形
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill="white", outline="", tags="bubble")
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill="white", outline="", tags="bubble")
    canvas.create_oval(x1, y1, x1 + 2*r, y1 + 2*r, fill="white", outline="", tags="bubble")
    canvas.create_oval(x2 - 2*r, y1, x2, y1 + 2*r, fill="white", outline="", tags="bubble")
    canvas.create_oval(x1, y2 - 2*r, x1 + 2*r, y2, fill="white", outline="", tags="bubble")
    canvas.create_oval(x2 - 2*r, y2 - 2*r, x2, y2, fill="white", outline="", tags="bubble")

    # 边框
    canvas.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, style="arc",
                     outline="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, style="arc",
                     outline="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, style="arc",
                     outline="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, style="arc",
                     outline="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_line(x1 + r, y1, x2 - r, y1, fill="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_line(x1 + r, y2, x2 - r, y2, fill="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_line(x1, y1 + r, x1, y2 - r, fill="#CCCCCC", width=1.5, tags="bubble")
    canvas.create_line(x2, y1 + r, x2, y2 - r, fill="#CCCCCC", width=1.5, tags="bubble")

    # 小三角
    canvas.create_polygon(
        bubble_x - 6, y2,
        bubble_x + 6, y2,
        bubble_x, y2 + 10,
        fill="white", outline="#CCCCCC", tags="bubble"
    )
    # 遮住三角和矩形的交接线
    canvas.create_line(bubble_x - 6, y2, bubble_x + 6, y2,
                      fill="white", width=2, tags="bubble")

    # 文字
    canvas.create_text(
        bubble_x, (y1 + y2) / 2,
        text=text, fill="#333333",
        font=("Microsoft YaHei", font_size),
        tags="bubble"
    )


def draw_status_indicator(canvas, state, x, y):
    """绘制状态小图标"""
    canvas.delete("status_icon")

    icons = {
        STATE_HAPPY: "😊",
        STATE_HUNGRY: "🍽",
        STATE_SLEEPY: "💤",
        STATE_DIRTY: "🧹",
        STATE_SICK: "🤒",
    }

    icon = icons.get(state)
    if icon:
        canvas.create_text(
            x, y, text=icon,
            font=("Segoe UI Emoji", 14),
            tags="status_icon"
        )


def draw_skill_effect(canvas, skill_name, cx, cy, frame):
    """绘制技能特效"""
    canvas.delete("skill_effect")

    if not skill_name:
        return

    import math
    # 旋转星星特效
    for i in range(3):
        angle = (frame * 30 + i * 120) * math.pi / 180
        r = 35
        sx = cx + r * math.cos(angle)
        sy = cy + r * math.sin(angle)
        canvas.create_text(
            sx, sy, text="✨",
            font=("Segoe UI Emoji", 10),
            tags="skill_effect"
        )
