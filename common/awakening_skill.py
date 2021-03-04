from enum import Enum


AWAKENING_SKILL_MAP = {
    1: {'n': 'HP强化'},
    2: {'n': '攻击强化'},
    3: {'n': '回复强化'},

    4: {'n': '火伤害减轻'},
    5: {'n': '水伤害减轻'},
    6: {'n': '木伤害减轻'},
    7: {'n': '光伤害减轻'},
    8: {'n': '暗伤害减轻'},

    9: {'n': '自动回复'},
    10: {'n': '绑定耐性', 'plus': {'id': 52, 'v': 2}},
    11: {'n': '黑暗耐性', 'plus': {'id': 68, 'v': 5}},
    12: {'n': '妨碍耐性', 'plus': {'id': 69, 'v': 5}},
    13: {'n': '毒耐性', 'plus': {'id': 70, 'v': 5}},

    14: {'n': '火宝珠强化'},
    15: {'n': '水宝珠强化'},
    16: {'n': '木宝珠强化'},
    17: {'n': '光宝珠强化'},
    18: {'n': '暗宝珠强化'},

    19: {'n': '操作时间延长', 'plus': {'id': 53, 'v': 2}},
    20: {'n': '绑定回复'},
    21: {'n': '技能加速', 'plus': {'id': 56, 'v': 2}},

    22: {'n': '火属性强化'},
    23: {'n': '水属性强化'},
    24: {'n': '木属性强化'},
    25: {'n': '光属性强化'},
    26: {'n': '暗属性强化'},

    27: {'n': '2体攻击'},
    28: {'n': '封印耐性'},
    29: {'n': '回复宝珠强化'},
    30: {'n': '联机增幅'},

    31: {'n': '龙杀手'},
    32: {'n': '神杀手'},
    33: {'n': '恶魔杀手'},
    34: {'n': '机械杀手'},
    35: {'n': '平衡杀手'},
    36: {'n': '攻击杀手'},
    37: {'n': '体力杀手'},
    38: {'n': '回复杀手'},

    39: {'n': '进化用杀手'},
    40: {'n': '能力觉醒用杀手'},
    41: {'n': '强化合成用杀手'},
    42: {'n': '贩卖用杀手'},

    43: {'n': '连击强化'},
    44: {'n': '防御破坏'},
    45: {'n': '追加攻击'},
    46: {'n': '队伍HP强化'},
    47: {'n': '队伍回复强化'},
    48: {'n': '伤害无效贯通'},
    49: {'n': '辅助觉醒'},
    50: {'n': '超追加攻击'},
    51: {'n': '技能充能'},
    52: {'n': '绑定耐性＋'},
    53: {'n': '操作时间延长＋'},
    54: {'n': '云耐性'},
    55: {'n': '操作不可耐性'},

    56: {'n': '技能加速＋'},
    57: {'n': 'HP80%以上强化'},
    58: {'n': 'HP50%以下强化'},

    59: {'n': '回复L形消'},
    60: {'n': 'L形消攻击'},
    61: {'n': '超连击强化'},
    62: {'n': '连击宝珠生成'},
    63: {'n': '技能语音'},
    64: {'n': '地城奖励'},

    65: {'n': 'HP弱化'},
    66: {'n': '攻击弱化'},
    67: {'n': '回复弱化'},

    68: {'n': '黑暗耐性＋'},
    69: {'n': '妨碍耐性＋'},
    70: {'n': '毒耐性＋'},

    71: {'n': '妨碍宝珠的加护'},
    72: {'n': '毒宝珠的加护'},
}

# 等价表
AW_SK_EQUIVALENCE_TABLE = {
    52: {'n': '绑定耐性＋', 'plus': {'id': 10, 'v': 2}},
    53: {'n': '操作时间延长＋', 'plus': {'id': 19, 'v': 2}},
    56: {'n': '技能加速＋', 'plus': {'id': 21, 'v': 2}},
    68: {'n': '黑暗耐性＋', 'plus': {'id': 11, 'v': 5}},
    69: {'n': '妨碍耐性＋', 'plus': {'id': 12, 'v': 5}},
    70: {'n': '毒耐性＋', 'plus': {'id': 13, 'v': 5}},
}


def get_awakening_skill_value(aw_sk_id):
    if aw_sk_id in AW_SK_EQUIVALENCE_TABLE and AW_SK_EQUIVALENCE_TABLE[aw_sk_id].get('plus'):
        return AW_SK_EQUIVALENCE_TABLE[aw_sk_id]['plus']['id'], AW_SK_EQUIVALENCE_TABLE[aw_sk_id]['plus']['v']
    else:
        return aw_sk_id, 1


class Awakening(Enum):
    ENHANCED_HP = 1  # HP+500
    ENHANCED_ATK = 2  # 攻击力+100
    ENHANCED_RCV = 3  # 回复力+200

    REDUCE_FIRE_DMG = 4  # 火属性伤害-7%
    REDUCE_WATER_DMG = 5  # 水属性伤害-7%
    REDUCE_WOOD_DMG = 6  # 木属性伤害-7%
    REDUCE_LIGHT_DMG = 7  # 光属性伤害-7%
    REDUCE_DARK_DMG = 8  # 暗属性伤害-7%

    AUTO_RECOVER = 9  # 消除宝珠的回合，回复1000HP
    RESIST_BIND = 10  # 50%无效化绑定
    RESIST_DARK = 11  # 20%几率无效化黑暗攻击
    RESIST_JAMMERS = 12  # 20%几率无效化废珠攻击
    RESIST_POISON = 13  # 20%几率中毒攻击

    ENHANCED_FIRE_ORB = 14  # 火属性宝珠强化
    ENHANCED_WATER_ORB = 15  # 水属性宝珠强化
    ENHANCED_WOOD_ORB = 16  # 木属性宝珠强化
    ENHANCED_LIGHT_ORB = 17  # 光属性宝珠强化
    ENHANCED_DARK_ORB = 18  # 暗属性宝珠强化

    EXTEND_TIME = 19  # 操作时间延长0.5秒
    RECOVER_BIND = 20  # 一横行回复3回合绑定状态
    SKILL_BOOST = 21  # 技能加速 +1

    ENHANCED_FIRE_ATTR = 22  # 火属性横行强化
    ENHANCED_WATER_ATTR = 23  # 水属性横行强化
    ENHANCED_WOOD_ATTR = 24  # 木属性横行强化
    ENHANCED_LIGHT_ATTR = 25  # 光属性横行强化
    ENHANCED_DARK_ATTR = 26  # 暗属性横行强化

    TWO_WAY = 27  # 两体攻击
    RESIST_SKILL_BIND = 28  # 技能封印耐性 20%
    ENHANCED_HEART_ORB = 29  # 回复宝珠强化
    MULTI_BOOST = 30  # 协力强化

    DRAGON_KILLER = 31  # 龙杀
    GOD_KILLER = 32  # 神杀
    DEMON_KILLER = 33  # 恶魔杀
    MACHINE_KILLER = 34  # 机械杀
    BALANCE_KILLER = 35  # 平衡杀
    ATTACKER_KILLER = 36  # 攻击杀
    TANK_KILLER = 37  # 体力杀
    HEALER_KILLER = 38  # 回复杀

    EVOLVE_MATERIAL_KILLER = 39  # 进化素材杀
    AWAKEN_MATERIAL_KILLER = 40  # 觉醒素材杀
    ENHANCE_MATERIAL_KILLER = 41  # 强化素材杀
    VENDOR_MATERIAL_KILLER = 42  # 卖店用素材杀

    ENHANCED_COMBO = 43  # 7combo强化
    GUARD_BREAK = 44  # 追加攻击
    BONUS_ATTACK = 45  # 一列心追击
    ENHANCED_TEAM_HP = 46  # 队伍HP +5%
    ENHANCED_TEAM_RCV = 47  # 队伍回复力 +5%
    VOID_DAMAGE_PIERCER = 48  # 3x3无效穿透
    AWOKEN_ASSIST = 49  # 装备
    SUPER_BONUS_ATTACK = 50  # 超追加攻击
    SKILL_CHARGE = 51  # 五色技能充能
    RESIST_BIND_PLUS = 52  #
    EXTEND_TIME_PLUS = 53
    RESIST_CLOUD = 54
    RESIST_IMMOBILITY = 55  # 操作不可耐性

    SKILL_BOOST_PLUS = 56
    EIGHTY_HP_ENHANCED = 57
    FIFTY_HP_ENHANCED = 58

    L_SHIELD = 59
    L_ATTACK = 60
    ENHANCED_10_COMBO = 61
    COMBO_DROP = 62
    SKILL_VOICE = 63
    DUNGEON_BONUS = 64

    REDUCE_HP = 65
    REDUCE_ATK = 66
    REDUCE_RCV = 67

    RESIST_DARK_PLUS = 68
    RESIST_JAMMERS_PLUS = 69
    RESIST_POISON_PLUS = 70

    JAMMERS_ORBS_BLESSING = 71
    POISON_ORBS_BLESSING = 72



# const _AWAKENING_DAMAGE_MAP = new Map([
#   [Awakening.TWO_WAY, 1.5],
#   [Awakening.MULTI_BOOST, 1.5],
#   [Awakening.L_ATTACK, 1.5],
#   [Awakening.EIGHTY_HP_ENHANCED, 1.5],
#
#   [Awakening.ENHANCED_COMBO, 2],
#   [Awakening.SUPER_BONUS_ATTACK, 2],
#   [Awakening.FIFTY_HP_ENHANCED, 2],
#   [Awakening.JAMMERS_ORBS_BLESSING, 2],
#   [Awakening.POISON_ORBS_BLESSING, 2],
#
#   [Awakening.VOID_DAMAGE_PIERCER, 2.5],
#
#   [Awakening.ENHANCED_10_COMBO, 5],
# ]);
