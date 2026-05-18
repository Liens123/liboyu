"""桌面宠物 - 存档系统"""

import json
import os
import time
from config import SAVE_DIR, SAVE_FILE
from pet import Pet


def ensure_save_dir():
    """确保存档目录存在"""
    os.makedirs(SAVE_DIR, exist_ok=True)


def save_game(pet, window_pos=None):
    """保存游戏数据

    Args:
        pet: Pet 对象
        window_pos: 窗口位置 (x, y)
    """
    ensure_save_dir()

    data = {
        "pet": pet.to_dict(),
        "window_pos": window_pos,
        "save_time": time.time(),
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存失败: {e}")


def load_game():
    """加载游戏数据

    Returns:
        tuple: (Pet对象, 窗口位置) 或 (None, None) 如果没有存档
    """
    if not os.path.exists(SAVE_FILE):
        return None, None

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        pet_data = data.get("pet", {})
        pet = Pet.from_dict(pet_data)
        window_pos = data.get("window_pos")

        return pet, window_pos

    except Exception as e:
        print(f"加载存档失败: {e}")
        return None, None


def delete_save():
    """删除存档"""
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
        except Exception as e:
            print(f"删除存档失败: {e}")


def has_save():
    """检查是否有存档"""
    return os.path.exists(SAVE_FILE)
