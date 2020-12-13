import math
from typing import NewType
from enum import Enum


# 原始数据类型
ElementId = NewType('ElementId', int)
TypeId = NewType('TypeId', int)
CardId = NewType('CardId', int)
SkillId = NewType('SkillId', int)
PetInfo = NewType('PetInfo', dict)


ELEMENT_MAP = {
    0: '火',
    1: '水',
    2: '木',
    3: '光',
    4: '暗',
}

TYPE_MAP = {
    0: '进化用',
    1: '平衡',
    2: '体力',
    3: '回复',
    4: '龙',
    5: '神',
    6: '攻击',
    7: '恶魔',
    8: '机械',
    12: '能力觉醒用',
    14: '强化合成用',
    15: '贩卖用',
}

ORB_MAP = {
    0: '火',
    1: '水',
    2: '木',
    3: '光',
    4: '暗',
    5: '回复',
    6: '废',
    7: '毒',
    8: '猛毒',
    9: '炸弹',
}


class Printable(object):
    """Simple way to make an object printable."""
    pass

    # def __repr__(self):
    #     return '{}({})'.format(self.__class__.__name__, dump_helper(self))

    # def __str__(self):
    #     return self.__repr__()


class Curve(Printable):
    """Describes how to scale according to level 1-10."""

    def __init__(self,
                 min_value: int,
                 max_value: int = None,
                 scale: float = 1.0,
                 max_level: int = 10,
                 limit_mult: int = 0):
        self.min_value = min_value
        self.max_value = max_value or min_value * max_level
        self.scale = scale
        self.max_level = max(max_level, 1)
        self.limit_mult = limit_mult / 10

    def value_at(self, level: int):
        if level <= self.max_level:
            f = 1 if self.max_level == 1 else ((level - 1) / (self.max_level - 1))
            return int(round(self.min_value + (self.max_value - self.min_value) * math.pow(f, self.scale)))
        else:
            pass
