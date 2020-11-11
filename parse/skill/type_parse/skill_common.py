from common.awakening_skill import AWAKENING_SKILL_MAP


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
    if element_id < 5:
        return f'{ELEMENT_MAP[element_id]}属性'
    else:
        return '回复力'


def element_buff(element_id):
    if element_id < 5:
        return f'{element(element_id)}攻击力'
    else:
        return element(element_id)


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
        'random': 0,  # 随机生成数量
        'row': False,  # 行
        'column': False,  # 列
        'all': False,  # 洗版
        'refresh': False,  # 刷新
        'shape': False,  # 形状
    }


# 转换flag为对应表
# 默认用来转换宝珠的10格表
def bitmap_to_flag_array(flags, max_len=10):
    flag_list = []
    bit = 1
    for i in range(max_len):
        flag_list.append(int(bool(flags & bit)))
        bit *= 2
    return flag_list


# 转换list为宝珠对应表
def list_to_orb_array(orb_list):
    orb_array = bitmap_to_flag_array(0)
    for orb_id in orb_list:
        if orb_id == -1:
            break
        orb_array[orb_id] = True
    return orb_array


# 2个orb_array求并集
def union_array(orb_array1, orb_array2):
    new_orb_array = []
    assert len(orb_array1) == len(orb_array2)
    for i in range(0, len(orb_array1)):
        new_orb_array.append(orb_array1[i] or orb_array2[i])
    return new_orb_array


# 根据orb_array生成一个列表
# TODO：更多个性化
def get_enable_orb_text(orb_array):
    orb_text_list = []
    for index, is_up in enumerate(orb_array):
        if is_up:
            orb_text_list.append(f'{ORB_MAP[index]}宝珠')
    return '、'.join(orb_text_list)


# 根据array生成一个描述列的文字
def get_col_text(col_array):
    col_text_list = []
    # 0/1/2是左3列
    if col_array[:3] == [1, 0, 0]:
        col_text_list.append('左数第1列')
    elif col_array[:3] == [0, 1, 0]:
        col_text_list.append('左数第2列')
    elif col_array[:3] == [1, 1, 0]:
        col_text_list.append('最左边的两列')
    elif col_array[:3] == [0, 0, 1]:
        col_text_list.append('左数第3列')
    elif col_array[:3] == [1, 0, 1]:
        col_text_list.append('左数第1和第3列')
    elif col_array[:3] == [0, 1, 1]:
        col_text_list.append('左数第2和第3列')
    elif col_array[:3] == [1, 1, 1]:
        col_text_list.append('最左边的三列')

    # 5/4/3是右3列
    if col_array[3:] == [0, 0, 1]:
        col_text_list.append('右数第1列')
    elif col_array[3:] == [0, 1, 0]:
        col_text_list.append('右数第2列')
    elif col_array[3:] == [0, 1, 1]:
        col_text_list.append('最右边的两列')
    elif col_array[3:] == [1, 0, 0]:
        col_text_list.append('右数第3列')
    elif col_array[3:] == [1, 0, 1]:
        col_text_list.append('右数第1和第3列')
    elif col_array[3:] == [1, 1, 0]:
        col_text_list.append('右数第2和第3列')
    elif col_array[3:] == [1, 1, 1]:
        col_text_list.append('最左边的三列')

    return '和'.join(col_text_list)


# 根据array生成一个描述行的文字
def get_row_text(row_array):
    row_text_list = []
    # 0/1是上2行
    if row_array[:2] == [1, 0]:
        row_text_list.append('上数第1行')
    elif row_array[:2] == [0, 1]:
        row_text_list.append('上数第2行')
    elif row_array[:2] == [1, 1]:
        row_text_list.append('最上边的两行')

    # 2是中间行
    if row_array[2] == 1:
        row_text_list.append('正中间的一行')

    # 4/3是下2行
    if row_array[3:] == [0, 1]:
        row_text_list.append('下数第1行')
    elif row_array[3:] == [1, 0]:
        row_text_list.append('下数第2行')
    elif row_array[3:] == [1, 1]:
        row_text_list.append('最下边的两行')

    if len(row_text_list) == 1:
        return row_text_list[0]
    else:
        return f'{"、".join(row_text_list[:-1])}和{row_text_list[-1]}'


# 根据array生成一个描述属性的文字
def get_ele_atk_text(ele_array):
    row_text_list = []
    if sum(ele_array) == len(ele_array):
        return '全属性总攻击力'
    else:
        for ele_id, has_ele in enumerate(ele_array):
            if has_ele:
                row_text_list.append(f'{ELEMENT_MAP[ele_id]}属性')

    if len(row_text_list) == 1:
        return f'{row_text_list[0]}攻击力'
    else:
        return f'{"、".join(row_text_list[:-1])}和{row_text_list[-1]}总攻击力'


# 获得一个空的攻击力buff表
def get_blank_atk_buff_map():
    return {
        0: False,  # 火,
        1: False,  # 水,
        2: False,  # 木,
        3: False,  # 光
        4: False,  # 暗,
        5: False,  # 回复力
        11: False,  # 平衡,
        12: False,  # 体力,
        13: False,  # 回复,
        14: False,  # 龙,
        15: False,  # 神,
        16: False,  # 攻击,
        17: False,  # 恶魔,
        18: False,  # 机械,
        't': 0,  # 回合数
        'm': 0,  # 倍率
    }


# 获得一个空的攻宝珠buff表
def get_blank_orb_buff_map():
    return {
        0: False,  # 火,
        1: False,  # 水,
        2: False,  # 木,
        3: False,  # 光,
        4: False,  # 暗,
        5: False,  # 心
        'm': 0,  # 强化倍率
    }


# 形状描述表
SHAPE_CODE_MAP = {
    '2-7-2-0-0': ['在盘面左上角以十字形', 0],
    '16-56-16-0-0': ['在盘面右上角以十字形', 0],
    '0-0-2-7-2': ['在盘面左下角以十字形', 0],
    '0-0-16-56-16': ['在盘面右下角以十字形', 0],

    '7-1-1-0-0': ['在盘面左上角以L形', 1],
    '56-32-32-0-0': ['在盘面右上角以L形', 1],
    '0-0-1-1-7': ['在盘面左下角以L形', 1],
    '0-0-32-32-56': ['在盘面右下角以L形', 1],
    '56-32-33-1-7': ['在盘面右上角和左下角以L形', 1],

    '7-7-7-0-0': ['在盘面左上角以3x3矩形（7x6盘时是3x4）', 2],
    '0-0-7-7-7': ['在盘面左下角以3x3矩形（7x6盘时是3x4）', 2],
    '56-56-56-0-0': ['在盘面右下角以3x3矩形（7x6盘时是3x4）', 2],
    '0-0-56-56-56': ['在盘面右下角以3x3矩形（7x6盘时是3x4）', 2],
    '0-7-7-7-0': ['在盘面左侧中间以3x3矩形（7x6盘时是3x4）', 2],

    '63-33-33-33-63': ['在盘面最外圈', 99],
    '33-0-0-0-33': ['在盘面四角', 99],
    '56-40-32-32-0': ['在盘面右上角以7形', 99],
}


# 生成形状的描述文字
def get_shape_info(shape_array):
    code = '-'.join([str(i) for i in shape_array])
    if code not in SHAPE_CODE_MAP:
        raise Exception(f'新形状：{code}')
    else:
        return SHAPE_CODE_MAP[code]
