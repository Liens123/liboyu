"""桌面宠物 - 宠物核心逻辑"""

import time
import random
from config import (
    MAX_STAT, MIN_STAT,
    HUNGER_DECAY_INTERVAL, HUNGER_DECAY_AMOUNT,
    MOOD_DECAY_INTERVAL, MOOD_DECAY_AMOUNT,
    CLEANLINESS_DECAY_INTERVAL, CLEANLINESS_DECAY_AMOUNT,
    HEALTH_DECAY_INTERVAL, HEALTH_DECAY_AMOUNT,
    HEALTH_RECOVER_INTERVAL, HEALTH_RECOVER_AMOUNT,
    FEED_AMOUNT, PLAY_AMOUNT, CLEAN_AMOUNT, HEAL_AMOUNT,
    EXP_PER_ACTION, EXP_BASE, EXP_GROWTH,
    STAGES, SKILLS,
    STATE_IDLE, STATE_HAPPY, STATE_HUNGRY, STATE_SLEEPY, STATE_DIRTY, STATE_SICK,
    BUBBLE_TEXTS, BUBBLE_INTERVAL, BUBBLE_DURATION,
)


class Pet:
    """宠物实体，管理所有属性和状态"""

    def __init__(self, name="小猫咪"):
        self.name = name

        # 核心属性
        self.hunger = 80
        self.mood = 80
        self.cleanliness = 80
        self.health = 100
        self.exp = 0
        self.level = 1

        # 技能列表
        self.skills = []

        # 状态
        self.state = STATE_IDLE
        self.is_sleeping = False

        # 时间戳
        self.last_hunger_decay = time.time()
        self.last_mood_decay = time.time()
        self.last_cleanliness_decay = time.time()
        self.last_health_decay = time.time()
        self.last_health_recover = time.time()
        self.last_bubble_time = time.time()

        # 气泡
        self.bubble_text = ""
        self.bubble_visible = False
        self.bubble_start_time = 0

        # 动画状态
        self.anim_frame = 0
        self.anim_timer = time.time()
        self.performing_skill = False
        self.current_skill = None
        self.skill_start_time = 0

    @property
    def stage(self):
        """根据等级返回当前成长阶段"""
        for key, info in STAGES.items():
            if info["min_level"] <= self.level <= info["max_level"]:
                return key
        return "senior"

    @property
    def stage_info(self):
        """返回当前成长阶段信息"""
        return STAGES[self.stage]

    @property
    def exp_to_next_level(self):
        """返回升到下一级所需经验"""
        return int(EXP_BASE * (EXP_GROWTH ** (self.level - 1)))

    @property
    def exp_progress(self):
        """返回当前等级的经验进度（0.0-1.0）"""
        return min(self.exp / self.exp_to_next_level, 1.0)

    def update(self):
        """每帧调用，更新属性衰减、状态判定、气泡"""
        now = time.time()

        # 属性衰减
        if now - self.last_hunger_decay >= HUNGER_DECAY_INTERVAL:
            self.hunger = max(MIN_STAT, self.hunger - HUNGER_DECAY_AMOUNT)
            self.last_hunger_decay = now

        if now - self.last_mood_decay >= MOOD_DECAY_INTERVAL:
            self.mood = max(MIN_STAT, self.mood - MOOD_DECAY_AMOUNT)
            self.last_mood_decay = now

        if now - self.last_cleanliness_decay >= CLEANLINESS_DECAY_INTERVAL:
            self.cleanliness = max(MIN_STAT, self.cleanliness - CLEANLINESS_DECAY_AMOUNT)
            self.last_cleanliness_decay = now

        # 健康值：饥饿<30时衰减，否则恢复
        if self.hunger < 30:
            if now - self.last_health_decay >= HEALTH_DECAY_INTERVAL:
                self.health = max(MIN_STAT, self.health - HEALTH_DECAY_AMOUNT)
                self.last_health_decay = now
        else:
            if now - self.last_health_recover >= HEALTH_RECOVER_INTERVAL:
                self.health = min(MAX_STAT, self.health + HEALTH_RECOVER_AMOUNT)
                self.last_health_recover = now

        # 更新状态
        self._update_state()

        # 气泡逻辑
        if self.bubble_visible:
            if now - self.bubble_start_time >= BUBBLE_DURATION:
                self.bubble_visible = False
                self.bubble_text = ""
        else:
            if now - self.last_bubble_time >= BUBBLE_INTERVAL:
                self._show_random_bubble()

        # 动画帧更新
        if now - self.anim_timer >= 0.5:
            self.anim_frame = (self.anim_frame + 1) % 4
            self.anim_timer = now

        # 技能表演结束检测
        if self.performing_skill and now - self.skill_start_time >= 3.0:
            self.performing_skill = False
            self.current_skill = None

    def _update_state(self):
        """根据属性值判定当前状态"""
        if self.performing_skill:
            return  # 技能表演中不切换状态

        if self.health < 30:
            self.state = STATE_SICK
        elif self.hunger < 25:
            self.state = STATE_HUNGRY
        elif self.cleanliness < 25:
            self.state = STATE_DIRTY
        elif self.mood < 25:
            self.state = STATE_SLEEPY
        elif self.mood > 70 and self.hunger > 50:
            self.state = STATE_HAPPY
        else:
            self.state = STATE_IDLE

    def _show_random_bubble(self):
        """随机显示一个气泡台词"""
        texts = BUBBLE_TEXTS.get(self.state, BUBBLE_TEXTS[STATE_IDLE])
        self.bubble_text = random.choice(texts)
        self.bubble_visible = True
        self.bubble_start_time = time.time()
        self.last_bubble_time = time.time()

    def _add_exp(self, amount):
        """增加经验值，处理升级"""
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level += 1
            # 检查是否解锁新技能
            if self.level in SKILLS:
                skill = SKILLS[self.level]
                if skill["name"] not in [s["name"] for s in self.skills]:
                    self.skills.append(skill)
                    self.bubble_text = f"学会了新技能：{skill['name']}！"
                    self.bubble_visible = True
                    self.bubble_start_time = time.time()

    def _clamp_stat(self, value):
        """将属性值限制在有效范围内"""
        return max(MIN_STAT, min(MAX_STAT, value))

    # === 互动操作 ===

    def feed(self):
        """喂食"""
        self.hunger = self._clamp_stat(self.hunger + FEED_AMOUNT)
        self.mood = self._clamp_stat(self.mood + 3)
        self._add_exp(EXP_PER_ACTION)
        self.bubble_text = "好好吃！谢谢~"
        self.bubble_visible = True
        self.bubble_start_time = time.time()

    def play(self):
        """玩耍"""
        self.mood = self._clamp_stat(self.mood + PLAY_AMOUNT)
        self.hunger = max(MIN_STAT, self.hunger - 3)
        self._add_exp(EXP_PER_ACTION)
        self.bubble_text = "好开心呀！再来一次！"
        self.bubble_visible = True
        self.bubble_start_time = time.time()

    def clean(self):
        """清洁"""
        self.cleanliness = self._clamp_stat(self.cleanliness + CLEAN_AMOUNT)
        self.mood = self._clamp_stat(self.mood + 2)
        self._add_exp(EXP_PER_ACTION)
        self.bubble_text = "好舒服~干净了！"
        self.bubble_visible = True
        self.bubble_start_time = time.time()

    def heal(self):
        """治疗"""
        self.health = self._clamp_stat(self.health + HEAL_AMOUNT)
        self._add_exp(EXP_PER_ACTION)
        self.bubble_text = "感觉好多了！"
        self.bubble_visible = True
        self.bubble_start_time = time.time()

    def perform_skill(self, skill_index):
        """表演技能"""
        if 0 <= skill_index < len(self.skills):
            self.performing_skill = True
            self.current_skill = self.skills[skill_index]
            self.skill_start_time = time.time()
            self._add_exp(EXP_PER_ACTION * 2)
            self.mood = self._clamp_stat(self.mood + 5)
            self.bubble_text = f"看我的{self.current_skill['name']}！"
            self.bubble_visible = True
            self.bubble_start_time = time.time()

    # === 序列化 ===

    def to_dict(self):
        """转为字典，用于保存"""
        return {
            "name": self.name,
            "hunger": self.hunger,
            "mood": self.mood,
            "cleanliness": self.cleanliness,
            "health": self.health,
            "exp": self.exp,
            "level": self.level,
            "skills": self.skills,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典恢复"""
        pet = cls(data.get("name", "小猫咪"))
        pet.hunger = data.get("hunger", 80)
        pet.mood = data.get("mood", 80)
        pet.cleanliness = data.get("cleanliness", 80)
        pet.health = data.get("health", 100)
        pet.exp = data.get("exp", 0)
        pet.level = data.get("level", 1)
        pet.skills = data.get("skills", [])
        return pet
