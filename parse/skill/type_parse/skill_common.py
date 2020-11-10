from common.pad_types import OrbType, TurnType


ELEMENT_MAP = {
    0: '火',
    1: '水',
    2: '木',
    3: '光',
    4: '暗',
}

TYPE_MAP = {
    1: '平衡',
    2: '体力',
    3: '回复',
    4: '龙',
    5: '神',
    6: '攻击',
    7: '恶魔',
    8: '机械',
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


def element(element_id):
    return f'{ELEMENT_MAP[element_id]}属性'


def monster_type(type_id):
    return f'{TYPE_MAP[type_id]}类'


def orb_buff(drop_id):
    assert 0 <= drop_id <= 5
    if drop_id == 5:
        return '回复力'
    else:
        return f'{ELEMENT_MAP[drop_id]}属性攻击力'


def orb(drop_id):
    return f'{ORB_MAP[drop_id]}宝珠'


# 除以一个数获得描述用值（int或是float）
def get_times(number, multi=100):
    number = number/multi
    if int(number) == number:
        number = int(number)
    return number


# 给数组补0
def add_zero(array, length):
    while len(array) < length:
        array.append(0)


# 获得一个基础的宝珠转换类型表
def get_blank_turn_type_map():
    return {
        'count': 0,  # 转换特定X种
        'random': 0,  # 随机生成
        'row': False,  # 横行
        'column': False,  # 竖列
        'all': False,  # 洗版
        'refresh': False,  # 刷新
    }


# 转换flag为宝珠对应表
def flag_to_orb_array(flags):
    return [
        bool(flags & 1),  # 火
        bool(flags & 2),  # 水
        bool(flags & 4),  # 木
        bool(flags & 8),  # 光
        bool(flags & 16),  # 暗
        bool(flags & 32),  # 心
        bool(flags & 64),  # 废
        bool(flags & 128),  # 毒
        bool(flags & 256),  # 猛毒
        bool(flags & 512),  # 炸弹
    ]


# 转换list为宝珠对应表
def list_to_orb_array(orb_list):
    orb_array = flag_to_orb_array(0)
    for orb_id in orb_list:
        if orb_id == -1:
            break
        orb_array[orb_id] = True
    return orb_array


# 2个orb_array求并集
def union_orb_array(orb_array1, orb_array2):
    new_orb_array = []
    assert len(orb_array1) == len(orb_array2)
    for i in range(0, len(orb_array1)):
        new_orb_array.append(orb_array1[i] and orb_array2[i])
    return new_orb_array


# 根据orb_array生成一个列表
# TODO：更多个性化
def get_enable_orb_text(orb_array):
    orb_text_list = []
    for index, is_up in enumerate(orb_array):
        if is_up:
            orb_text_list.append(f'{ORB_MAP[index]}宝珠')
    return '、'.join(orb_text_list)


# 转换flag为宝珠对应表
def get_blank_atk_buff_map():
    return {
        0: 0,  # 火,
        1: 0,  # 水,
        2: 0,  # 木,
        3: 0,  # 光,
        4: 0,  # 暗,
        11: 0,  # 平衡,
        12: 0,  # 体力,
        13: 0,  # 回复,
        14: 0,  # 龙,
        15: 0,  # 神,
        16: 0,  # 攻击,
        17: 0,  # 恶魔,
        18: 0,  # 机械,
        't': 0,
    }