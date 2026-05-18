"""桌面宠物 - 矢量渲染器（用 Canvas 形状绘制，更美观）"""

import tkinter as tk
import math
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    STATE_IDLE, STATE_HAPPY, STATE_HUNGRY, STATE_SLEEPY, STATE_DIRTY, STATE_SICK,
)

# 猫咪颜色方案
CAT_COLORS = {
    "body":      "#F09040",   # 橘猫主色（更温暖）
    "body_dark": "#D07830",   # 深橘
    "belly":     "#FFE8D0",   # 肚子浅色（对比更强）
    "ear_outer": "#F09040",   # 耳朵外侧
    "ear_inner": "#FFAAAA",   # 耳朵内侧粉（更粉）
    "eye_white": "#FFFFFF",   # 眼白
    "eye_pupil": "#1A1A2E",   # 瞳孔（深蓝黑）
    "eye_shine": "#FFFFFF",   # 眼睛高光
    "nose":      "#FF6B81",   # 鼻子粉（珊瑚色）
    "mouth":     "#CC4455",   # 嘴巴
    "whisker":   "#706050",   # 胡须（棕灰色）
    "outline":   "#2D1F15",   # 轮廓深色
    "cheek":     "#FFB0B0",   # 腮红（更浅）
    "tail":      "#D07830",   # 尾巴（深色区分）
    "paw":       "#FFE8D0",   # 爪子
    "fur_tuft":  "#FFD0A0",   # 毛簇
    "paw_bean":  "#FF8090",   # 脚掌豆
}


def _draw_cat_body(cx, cy, scale=1.0, frame=0, state=None):
    """绘制猫咪身体各部分，返回 Canvas 绘制指令列表"""
    s = scale
    parts = []

    # 预计算动画值
    blink = (frame % 80) in (0, 1, 2) if frame > 0 else False
    ear_twitch = 0
    if frame > 0 and frame % 60 in (0, 1, 2, 3):
        ear_twitch = 3 if frame % 60 < 2 else -1

    # 1. 尾巴（曲线，动画集成）
    tail_swing = math.sin(frame * 1.0) * 6 * s if frame > 0 else 0
    tail_sway = math.sin(frame * 0.5 + 1.0) * 4 * s if frame > 0 else 0
    tail_pts = [
        (cx - 22*s, cy + 42*s),
        (cx - 38*s + tail_swing*0.3, cy + 28*s),
        (cx - 50*s + tail_swing*0.7, cy + 12*s + tail_sway*0.5),
        (cx - 46*s + tail_swing, cy - 5*s + tail_sway),
    ]
    parts.append(("spline", tail_pts, CAT_COLORS["body_dark"], 5))

    # 2. 身体（更修长的椭圆）
    parts.append(("oval", cx - 28*s, cy + 5*s, cx + 28*s, cy + 63*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 2))

    # 3. 肚子
    parts.append(("oval", cx - 16*s, cy + 18*s, cx + 16*s, cy + 55*s,
                  CAT_COLORS["belly"], "", 0))

    # 4. 胸部毛簇
    parts.append(("oval", cx - 10*s, cy + 38*s, cx + 10*s, cy + 50*s,
                  CAT_COLORS["fur_tuft"], "", 0))

    # 5. 左耳（更尖的三角形）
    ear_l = [
        (cx - 26*s, cy - 18*s),
        (cx - 38*s + ear_twitch, cy - 58*s),
        (cx - 6*s, cy - 26*s),
    ]
    parts.append(("polygon", ear_l, CAT_COLORS["ear_outer"], CAT_COLORS["outline"], 2))

    # 左耳内部
    ear_l_inner = [
        (cx - 24*s, cy - 22*s),
        (cx - 34*s + ear_twitch*0.5, cy - 48*s),
        (cx - 12*s, cy - 28*s),
    ]
    parts.append(("polygon", ear_l_inner, CAT_COLORS["ear_inner"], "", 0))

    # 左耳毛簇
    ear_l_tuft = [
        (cx - 30*s, cy - 45*s),
        (cx - 36*s + ear_twitch*0.7, cy - 54*s),
        (cx - 25*s, cy - 48*s),
    ]
    parts.append(("polygon", ear_l_tuft, CAT_COLORS["ear_inner"], "", 0))

    # 6. 右耳
    ear_r = [
        (cx + 26*s, cy - 18*s),
        (cx + 38*s - ear_twitch, cy - 58*s),
        (cx + 6*s, cy - 26*s),
    ]
    parts.append(("polygon", ear_r, CAT_COLORS["ear_outer"], CAT_COLORS["outline"], 2))

    # 右耳内部
    ear_r_inner = [
        (cx + 24*s, cy - 22*s),
        (cx + 34*s - ear_twitch*0.5, cy - 48*s),
        (cx + 12*s, cy - 28*s),
    ]
    parts.append(("polygon", ear_r_inner, CAT_COLORS["ear_inner"], "", 0))

    # 右耳毛簇
    ear_r_tuft = [
        (cx + 30*s, cy - 45*s),
        (cx + 36*s - ear_twitch*0.7, cy - 54*s),
        (cx + 25*s, cy - 48*s),
    ]
    parts.append(("polygon", ear_r_tuft, CAT_COLORS["ear_inner"], "", 0))

    # 7. 头部（稍窄的椭圆）
    parts.append(("oval", cx - 29*s, cy - 30*s, cx + 29*s, cy + 16*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 2))

    # 8. 腮红（上移 2px）
    parts.append(("oval", cx - 27*s, cy - 2*s, cx - 17*s, cy + 6*s,
                  CAT_COLORS["cheek"], "", 0))
    parts.append(("oval", cx + 17*s, cy - 2*s, cx + 27*s, cy + 6*s,
                  CAT_COLORS["cheek"], "", 0))

    # 9. 眼睛（检查眨眼）
    if not blink:
        # 左眼白
        parts.append(("oval", cx - 22*s, cy - 17*s, cx - 5*s, cy + 4*s,
                      CAT_COLORS["eye_white"], CAT_COLORS["outline"], 1.5))
        # 左瞳孔（垂直猫瞳）
        parts.append(("oval", cx - 17*s, cy - 11*s, cx - 10*s, cy + 2*s,
                      CAT_COLORS["eye_pupil"], "", 0))
        # 左眼主高光
        parts.append(("oval", cx - 15*s, cy - 9*s, cx - 12*s, cy - 6*s,
                      CAT_COLORS["eye_shine"], "", 0))
        # 左眼副高光
        parts.append(("oval", cx - 12*s, cy + 0*s, cx - 11*s, cy + 1*s,
                      CAT_COLORS["eye_shine"], "", 0))

        # 右眼白
        parts.append(("oval", cx + 5*s, cy - 17*s, cx + 22*s, cy + 4*s,
                      CAT_COLORS["eye_white"], CAT_COLORS["outline"], 1.5))
        # 右瞳孔
        parts.append(("oval", cx + 10*s, cy - 11*s, cx + 17*s, cy + 2*s,
                      CAT_COLORS["eye_pupil"], "", 0))
        # 右眼主高光
        parts.append(("oval", cx + 12*s, cy - 9*s, cx + 15*s, cy - 6*s,
                      CAT_COLORS["eye_shine"], "", 0))
        # 右眼副高光
        parts.append(("oval", cx + 11*s, cy + 0*s, cx + 12*s, cy + 1*s,
                      CAT_COLORS["eye_shine"], "", 0))
    else:
        # 眨眼 - 闭眼弧线
        parts.append(("arc", cx - 22*s, cy - 17*s, cx - 5*s, cy + 4*s, 0, 180,
                      CAT_COLORS["eye_pupil"], 2))
        parts.append(("arc", cx + 5*s, cy - 17*s, cx + 22*s, cy + 4*s, 0, 180,
                      CAT_COLORS["eye_pupil"], 2))

    # 10. 鼻子（稍大）
    nose_pts = [
        (cx - 5*s, cy + 4*s),
        (cx + 5*s, cy + 4*s),
        (cx, cy + 11*s),
    ]
    parts.append(("polygon", nose_pts, CAT_COLORS["nose"], "", 0))

    # 鼻唇沟
    parts.append(("oval", cx - 2*s, cy + 10*s, cx + 2*s, cy + 13*s,
                  CAT_COLORS["body_dark"], "", 0))

    # 11. 嘴巴（W 形 + 连接线）
    parts.append(("line", cx, cy + 11*s, cx, cy + 14*s, CAT_COLORS["mouth"], 1))
    parts.append(("line", cx - 9*s, cy + 14*s, cx, cy + 18*s, CAT_COLORS["mouth"], 1.5))
    parts.append(("line", cx, cy + 18*s, cx + 9*s, cy + 14*s, CAT_COLORS["mouth"], 1.5))

    # 12. 胡须（平滑曲线）
    # 左胡须
    parts.append(("spline", [(cx - 28*s, cy + 6*s), (cx - 38*s, cy + 3*s), (cx - 52*s, cy + 0*s)],
                  CAT_COLORS["whisker"], 1))
    parts.append(("spline", [(cx - 28*s, cy + 9*s), (cx - 38*s, cy + 9*s), (cx - 52*s, cy + 9*s)],
                  CAT_COLORS["whisker"], 1))
    parts.append(("spline", [(cx - 28*s, cy + 12*s), (cx - 38*s, cy + 14*s), (cx - 52*s, cy + 18*s)],
                  CAT_COLORS["whisker"], 1))

    # 右胡须
    parts.append(("spline", [(cx + 28*s, cy + 6*s), (cx + 38*s, cy + 3*s), (cx + 52*s, cy + 0*s)],
                  CAT_COLORS["whisker"], 1))
    parts.append(("spline", [(cx + 28*s, cy + 9*s), (cx + 38*s, cy + 9*s), (cx + 52*s, cy + 9*s)],
                  CAT_COLORS["whisker"], 1))
    parts.append(("spline", [(cx + 28*s, cy + 12*s), (cx + 38*s, cy + 14*s), (cx + 52*s, cy + 18*s)],
                  CAT_COLORS["whisker"], 1))

    # 13. 左前腿（更长）
    parts.append(("oval", cx - 21*s, cy + 46*s, cx - 9*s, cy + 72*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 1.5))
    # 左爪子
    parts.append(("oval", cx - 20*s, cy + 66*s, cx - 10*s, cy + 74*s,
                  CAT_COLORS["paw"], CAT_COLORS["outline"], 1))
    # 左脚掌豆
    parts.append(("oval", cx - 18*s, cy + 69*s, cx - 16*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))
    parts.append(("oval", cx - 15*s, cy + 69*s, cx - 13*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))
    parts.append(("oval", cx - 12*s, cy + 69*s, cx - 10*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))

    # 14. 右前腿
    parts.append(("oval", cx + 9*s, cy + 46*s, cx + 21*s, cy + 72*s,
                  CAT_COLORS["body"], CAT_COLORS["outline"], 1.5))
    # 右爪子
    parts.append(("oval", cx + 10*s, cy + 66*s, cx + 20*s, cy + 74*s,
                  CAT_COLORS["paw"], CAT_COLORS["outline"], 1))
    # 右脚掌豆
    parts.append(("oval", cx + 10*s, cy + 69*s, cx + 12*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))
    parts.append(("oval", cx + 13*s, cy + 69*s, cx + 15*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))
    parts.append(("oval", cx + 16*s, cy + 69*s, cx + 18*s, cy + 72*s,
                  CAT_COLORS["paw_bean"], "", 0))

    return parts


def _draw_closed_eyes(canvas, cx, cy, s):
    """绘制闭眼（困倦/睡觉）"""
    # 左眼 - 弧线
    canvas.create_arc(
        cx - 22*s, cy - 17*s, cx - 5*s, cy + 4*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼 - 弧线
    canvas.create_arc(
        cx + 5*s, cy - 17*s, cx + 22*s, cy + 4*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )


def _draw_happy_eyes(canvas, cx, cy, s):
    """绘制开心眼睛（^_^ 形）"""
    # 左眼 - 弧线
    canvas.create_arc(
        cx - 22*s, cy - 17*s, cx - 5*s, cy + 4*s,
        start=180, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2.5, tags="pet"
    )
    # 右眼 - 弧线
    canvas.create_arc(
        cx + 5*s, cy - 17*s, cx + 22*s, cy + 4*s,
        start=180, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2.5, tags="pet"
    )


def _draw_sad_eyes(canvas, cx, cy, s):
    """绘制难过眼睛"""
    # 左眼 - 下垂弧线
    canvas.create_arc(
        cx - 22*s, cy - 20*s, cx - 5*s, cy + 1*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼
    canvas.create_arc(
        cx + 5*s, cy - 20*s, cx + 22*s, cy + 1*s,
        start=0, extent=180, style="arc",
        outline=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )


def _draw_sick_face(canvas, cx, cy, s):
    """绘制生病表情（X_X）"""
    # 左眼 X
    canvas.create_line(
        cx - 20*s, cy - 14*s, cx - 7*s, cy - 1*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    canvas.create_line(
        cx - 7*s, cy - 14*s, cx - 20*s, cy - 1*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    # 右眼 X
    canvas.create_line(
        cx + 7*s, cy - 14*s, cx + 20*s, cy - 1*s,
        fill=CAT_COLORS["eye_pupil"], width=2, tags="pet"
    )
    canvas.create_line(
        cx + 20*s, cy - 14*s, cx + 7*s, cy - 1*s,
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

    # 呼吸动画（根据状态调整）
    if state == STATE_SLEEPY:
        breathe_offset = math.sin(frame * 0.4) * 3  # 更慢更深
    elif state == STATE_HAPPY:
        breathe_offset = math.sin(frame * 1.2) * 2  # 更快
    elif state == STATE_SICK:
        breathe_offset = math.sin(frame * 0.6) * 1.5  # 无力
    else:
        breathe_offset = math.sin(frame * 0.8) * 2  # 默认

    # 状态特殊动画
    if state == STATE_HAPPY:
        bounce = abs(math.sin(frame * 2.0)) * 3
        cy -= bounce  # 开心弹跳
    elif state == STATE_SICK:
        wobble = math.sin(frame * 1.5) * 2
        cx += wobble  # 生病摇晃

    cy += breathe_offset

    # 绘制身体各部分
    parts = _draw_cat_body(cx, cy, s, frame, state)

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
        elif shape == "spline":
            _, points, fill, width = part
            flat = []
            for p in points:
                flat.extend(p)
            canvas.create_line(*flat, fill=fill, width=width, smooth=True,
                             splinesteps=12, tags="pet")
        elif shape == "arc":
            _, x1, y1, x2, y2, start, extent, fill, width = part
            canvas.create_arc(x1, y1, x2, y2, start=start, extent=extent,
                            style="arc", outline=fill, width=width, tags="pet")

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
        for _ in range(8):
            dx = random.randint(-20, 20)
            dy = random.randint(0, 40)
            size = random.randint(2, 4)
            canvas.create_oval(
                cx + dx*s - size, cy + dy*s - size,
                cx + dx*s + size, cy + dy*s + size,
                fill="#AAAAAA", outline="", tags="pet"
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
