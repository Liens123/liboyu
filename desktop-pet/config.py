"""桌面宠物 - 配置常量"""

import os

# === 路径 ===
APP_NAME = "DesktopPet"
SAVE_DIR = os.path.join(os.environ.get("APPDATA", "."), APP_NAME)
SAVE_FILE = os.path.join(SAVE_DIR, "save.json")

# === 窗口 ===
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 280
PIXEL_SIZE = 8          # 每个像素点的显示大小
CANVAS_WIDTH = 20       # 像素画宽度（像素格数）
CANVAS_HEIGHT = 20      # 像素画高度（像素格数）
FPS = 4                 # 动画帧率（降低以获得更自然的动画）

# === 属性范围 ===
MAX_STAT = 100
MIN_STAT = 0

# === 属性衰减（每次衰减的间隔秒数和减少量）===
HUNGER_DECAY_INTERVAL = 60
HUNGER_DECAY_AMOUNT = 2
MOOD_DECAY_INTERVAL = 90
MOOD_DECAY_AMOUNT = 1
CLEANLINESS_DECAY_INTERVAL = 120
CLEANLINESS_DECAY_AMOUNT = 1
HEALTH_DECAY_INTERVAL = 30
HEALTH_DECAY_AMOUNT = 1    # 仅在饥饿值<30时生效
HEALTH_RECOVER_INTERVAL = 60
HEALTH_RECOVER_AMOUNT = 1  # 饥饿值>=30时自然恢复

# === 互动恢复量 ===
FEED_AMOUNT = 20
PLAY_AMOUNT = 15
CLEAN_AMOUNT = 25
HEAL_AMOUNT = 30

# === 经验与等级 ===
EXP_PER_ACTION = 5
EXP_BASE = 20           # 升到下一级所需基础经验
EXP_GROWTH = 1.3        # 每级经验需求增长系数

# === 成长阶段 ===
STAGES = {
    "baby":    {"min_level": 1,  "max_level": 5,  "name": "幼年", "color": "#FFB6C1"},
    "child":   {"min_level": 6,  "max_level": 15, "name": "少年", "color": "#87CEEB"},
    "adult":   {"min_level": 16, "max_level": 30, "name": "成年", "color": "#98FB98"},
    "senior":  {"min_level": 31, "max_level": 999,"name": "老年", "color": "#DDA0DD"},
}

# === 技能 ===
SKILLS = {
    5:  {"name": "握手",  "icon": "🤝"},
    10: {"name": "翻滚",  "icon": "🔄"},
    15: {"name": "跳跃",  "icon": "⬆️"},
    20: {"name": "转圈",  "icon": "💫"},
    25: {"name": "装死",  "icon": "💀"},
    30: {"name": "后空翻","icon": "🤸"},
}

# === 状态 ===
STATE_IDLE = "idle"
STATE_HAPPY = "happy"
STATE_HUNGRY = "hungry"
STATE_SLEEPY = "sleepy"
STATE_DIRTY = "dirty"
STATE_SICK = "sick"

# === 颜色（像素画调色板）===
COLOR_BG = "#f0f0f0"
COLOR_OUTLINE = "#333333"
COLOR_BODY = "#FF9800"
COLOR_BODY_LIGHT = "#FFB74D"
COLOR_BELLY = "#FFE0B2"
COLOR_EYE = "#333333"
COLOR_EYE_WHITE = "#FFFFFF"
COLOR_NOSE = "#E91E63"
COLOR_EAR_INNER = "#FFB6C1"
COLOR_WHISKER = "#666666"
COLOR_MOUTH = "#D32F2F"

# === 气泡台词 ===
BUBBLE_TEXTS = {
    STATE_IDLE:    ["喵~", "好无聊啊...", "今天天气真好", "你在忙什么呀？", "zzZ..."],
    STATE_HAPPY:   ["好开心！", "喵喵喵~", "最喜欢你了！", "嘿嘿~", "生活真美好~"],
    STATE_HUNGRY:  ["肚子饿了...", "有吃的吗？", "好饿好饿...", "想吃小鱼干！", "饿扁了..."],
    STATE_SLEEPY:  ["好困...", "想睡觉了...", "打个盹吧...", "眼皮好重...", "晚安..."],
    STATE_DIRTY:   ["身上脏脏的...", "想洗个澡...", "喵...不舒服...", "帮我擦擦~"],
    STATE_SICK:    ["不舒服...", "头好晕...", "需要看医生...", "好难受...", "陪陪我..."],
}

# === 自动保存间隔（秒）===
AUTO_SAVE_INTERVAL = 300

# === 气泡显示间隔（秒）===
BUBBLE_INTERVAL = 15
BUBBLE_DURATION = 5
