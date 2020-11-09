"""
解析宠物技能数据
"""

import os
import re
from typing import Dict, List, Any
from danteng_lib import load_json
from common.pad_types import Printable, SkillId

from config import RAW_DATA_BASE_PATH

# 原始数据文件名
FILE_NAME = 'download_skill_data.json'


class MonsterSkill(Printable):
    def __init__(self, skill_id: int, raw: List[str]):
        self.skill_id = SkillId(skill_id)

        self.name = raw[0]
        self.description = convert_color_tag(raw[1])  # 带有格式的转换为颜色了，如果以后出现其他的再处理
        self.skill_type = int(raw[2])
        self.levels = int(raw[3]) or None
        self.turn_max = int(raw[4]) if self.levels else None
        self.turn_min = self.turn_max - (self.levels - 1) if self.levels else None
        self.params = raw[6:]


def load_skill_data() -> Dict[int, Any]:
    data_json = load_json(os.path.join(RAW_DATA_BASE_PATH, FILE_NAME))
    assert data_json
    skill_data = dict()
    for i, ms in enumerate(data_json['skill']):
        skill_data[i] = MonsterSkill(i, ms)
    return skill_data


def convert_color_tag(text):
    text = re.sub(r'\^([a-f0-9]{6})\^', r'<span style="color:#\1">', text)
    text = text.replace('^p', '</span>')
    return text
