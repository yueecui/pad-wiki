import math
from typing import NewType
from enum import Enum


# 原始数据类型
ElementId = NewType('ElementId', int)
TypeId = NewType('TypeId', int)
CardId = NewType('CardId', int)
SkillId = NewType('SkillId', int)
PetInfo = NewType('PetInfo', dict)


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
                 max_level: int = 10):
        self.min_value = min_value
        self.max_value = max_value or min_value * max_level
        self.scale = scale
        self.max_level = max(max_level, 1)

    def value_at(self, level: int):
        f = 1 if self.max_level == 1 else ((level - 1) / (self.max_level - 1))
        return int(round(self.min_value + (self.max_value - self.min_value) * math.pow(f, self.scale)))


# 进化类型
class EvoType(Enum):
    BASE = 0
    NORMAL = 1              # 进化
    ULT = 11                # 究极进化
    SUPER_ULT = 12          # 超究极进化
    REBIRTH = 21            # 转生进化
    SUPER_REBIRTH = 22      # 超转生进化
    DOT = 31                # 点阵进化
    ASSIST = 41             # 武装化


# 宝珠类型
class OrbType(Enum):
    FIRE_ORB = 0
    WATER_ORB = 1
    WOOD_ORB = 2
    LIGHT_ORB = 3
    DARK_ORB = 4
    HEAL_ORB = 5
    OBSTACLE_ORB = 6
    POISON_ORB = 7
    S_POISON_ORB = 8
    BOMB_ORB = 9


# 转换类型
class TurnType(Enum):
    COUNT = 0
    ROW = 1
    COLUMN = 2
    REFRESH = 3
    ALL = 4
