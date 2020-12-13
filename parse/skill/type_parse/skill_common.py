from common.awakening_skill import AWAKENING_SKILL_MAP
from common.pad_types import ELEMENT_MAP, TYPE_MAP, ORB_MAP


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


# 获得一个基础的宝珠转换类型表（作废）
def get_blank_turn_type_map():
    return [0, 0, 0, 0, 0, 0]
    # {
    #     'row': False,  # 行
    #     'column': False,  # 列
    #     'all': False,  # 洗版
    #     'color': False,  # 色转色
    #     'any':  False,  # 额外生成
    #     'shape': False,  # 形状
    # }


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
        orb_array[orb_id] = 1
    return orb_array


# 2个orb_array求并集
def union_array(orb_array1, orb_array2):
    new_orb_array = []
    assert len(orb_array1) == len(orb_array2)
    for i in range(0, len(orb_array1)):
        new_orb_array.append(orb_array1[i] or orb_array2[i])
    return new_orb_array


# 根据orb_array生成一个列表
def get_orb_text(orb_id):
    return f'<div class="orb-{orb_id}">{ORB_MAP[orb_id]}宝珠</div>'


# 根据orb_array生成一个列表
def get_enable_orb_text(orb_array):
    orb_text_list = []
    for index, is_up in enumerate(orb_array):
        if is_up:
            orb_text_list.append(get_orb_text(index))
    return ''.join(orb_text_list)


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


# 根据array生成一个觉醒技能序列文字
def get_awakening_skill_info(aw_sk_array):
    name_list = []
    extra_text_list = []
    for aw_id in aw_sk_array:
        if aw_id > 0:
            assert aw_id in AWAKENING_SKILL_MAP
            aw_sk_info = AWAKENING_SKILL_MAP[aw_id]
            name_list.append(aw_sk_info['n'])
            if aw_sk_info.get('plus'):
                extra_text_list.append(f'{AWAKENING_SKILL_MAP[aw_sk_info["plus"]["id"]]["n"]}视为{aw_sk_info["plus"]["v"]}个{aw_sk_info["n"]}')

    if len(name_list) == 1:
        name_text = f'{name_list[0]}'
    else:
        name_text = f'{"、".join(name_list[:-1])}和{name_list[-1]}'

    return [name_text, '，'.join(extra_text_list)]


# 获得一个空的攻击力buff表
def get_blank_atk_buff_map():
    return {
        # 填倍率
        'ele': [0, 0, 0, 0, 0, 0],
        'type': [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 第一位不用
        't': 0,  # 回合数
    }


# 获得一个空的攻宝珠buff表
def get_blank_orb_buff_map():
    return [0, 0, 0, 0, 0, 0]
    #
    #     0: 0,  # 火,
    #     1: 0,  # 水,
    #     2: 0,  # 木,
    #     3: 0,  # 光,
    #     4: 0,  # 暗,
    #     5: 0,  # 心
    #     'm': 0,  # 强化倍率
    # }


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
    '7-1-33-32-56': ['在盘面左上角和右下角以L形', 1],

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


# 转换flag为宠物分类表
def convert_pet_category(ele_flag=0, type_flag=0):
    if ele_flag == -1:
        ele_flag = 31
    if type_flag == -1:
        type_flag = 65535  # 2^16-1

    ele_list = bitmap_to_flag_array(ele_flag, 5)
    type_list = bitmap_to_flag_array(type_flag, 16)  # 八种类型，但0位不用

    return {
        0: ele_list[0],  # 火,
        1: ele_list[1],  # 水,
        2: ele_list[2],  # 木,
        3: ele_list[3],  # 光
        4: ele_list[4],  # 暗,
        10: type_list[0],  # 进化用
        11: type_list[1],  # 平衡,
        12: type_list[2],  # 体力,
        13: type_list[3],  # 回复,
        14: type_list[4],  # 龙,
        15: type_list[5],  # 神,
        16: type_list[6],  # 攻击,
        17: type_list[7],  # 恶魔,
        18: type_list[8],  # 机械,
        22: type_list[12],  # 能力觉醒用
        24: type_list[14],  # 强化合成用
        25: type_list[15],  # 贩卖用
        'total': sum(ele_list) + sum(type_list),
    }


# 合并第二个宠物分类到第一个
def union_pet_category(base_pet_category, merge_pet_category):
    for k, v in base_pet_category.items():
        if merge_pet_category.get(k):
            if type(k) == int:
                base_pet_category[k] = v or merge_pet_category[k]


# 生成队长技能描述宠物分类的
def get_pet_category_text(pet_category):
    category_list = []
    enable_count = 0
    for ele_id in range(5):
        if pet_category.get(ele_id):
            category_list.append(f'{ELEMENT_MAP[ele_id]}属性')
            enable_count += 1
    if enable_count == 5:
        return '所有'
    enable_count = 0
    for type_id in range(11, 26):
        if pet_category.get(type_id):
            category_list.append(f'{TYPE_MAP[type_id-10]}类')
    if enable_count == 12:
        return '所有'

    assert len(category_list) > 0
    if len(category_list) == 1:
        return category_list[0]
    else:
        return f'{"、".join(category_list[:-1])}和{category_list[-1]}'


# 获取空的队长buff效果
def get_blank_leader_buff():
    return {
        'hp': 1,  # HP倍率
        'ehp': 1,   # 有效HP倍率（HP倍率与全属性减伤共同计算）
        'atk': 1,  # 攻击力倍率
        'rec': 1,  # 回复力倍率
        'd_rate': 100,  # 受到伤害的百分比，注意分属性的是单独的
        # 'ele_d_rate': [100, 100, 100, 100, 100],  # 默认不生成，如果该项目存在，表示这个队长技能会减免特定属性伤害
        'time': 0,  # 额外移动时间
        'flat_add': 0,  # 固定追击（无视防御），0=无
        'atk_add': 0,   # 消珠追打，按自身攻击百分比，0=无，其他数字表示倍率
        'rec_add': 0,   # 消珠回血，按自身回复百分比
        'add_combo': 0,   # 额外加算combo
    }


# 2个leader_buff求并集
def union_leader_buff(base_leader_buff, merge_leader_buff):
    if 'ele_d_rate' in merge_leader_buff and 'ele_d_rate' not in base_leader_buff:
        base_leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]

    for k, v in base_leader_buff.items():
        if merge_leader_buff.get(k):
            if type(k) == int:
                base_leader_buff[k] = v or merge_leader_buff[k]
            elif k in ['hp', 'atk', 'rec']:
                if merge_leader_buff[k] > 0:
                    base_leader_buff[k] *= merge_leader_buff[k]
            elif k == 'd_rate':
                base_leader_buff[k] *= (merge_leader_buff[k] / 100)
                if int(base_leader_buff[k]) == base_leader_buff[k]:
                    base_leader_buff[k] = int(base_leader_buff[k])
            elif k == 'ele_d_rate':
                for i, rate in enumerate(merge_leader_buff[k]):
                    base_leader_buff[k][i] *= (merge_leader_buff[k][i] / 100)
                    if int(base_leader_buff[k][i]) == base_leader_buff[k][i]:
                        base_leader_buff[k][i] = int(base_leader_buff[k][i])
            elif k == 'time':
                base_leader_buff[k] += merge_leader_buff[k]
    # 如果ele_d_rate为有效值，则d_rate置为-1
    if 'ele_d_rate' in base_leader_buff and base_leader_buff['d_rate'] != -1:
        first_rate = base_leader_buff['ele_d_rate'][0]
        for rate in range(len(base_leader_buff['ele_d_rate'])):
            if rate != first_rate:
                base_leader_buff['d_rate'] = -1
                break
    # 计算有效血量
    base_leader_buff['ehp'] = base_leader_buff['hp'] / (base_leader_buff['d_rate'] / 100)


# 更新队长技能的效果
def update_leader_buff(result, leader_buff=None, pet_category=None):
    if leader_buff:
        if 'leader_buff' not in result['detail']:
            result['detail']['leader_buff'] = get_blank_leader_buff()
        union_leader_buff(result['detail']['leader_buff'], leader_buff)
    if pet_category:
        if 'pet_category' not in result['detail']:
            result['detail']['pet_category'] = convert_pet_category(0, 0)
        union_pet_category(result['detail']['pet_category'], pet_category)


# 获得宠物基本数值倍率描述
def get_pet_status_text(hp_m, atk_m, rec_m):
    temp_text = []
    if hp_m == atk_m == rec_m > 0:
        temp_text.append(f'全属性{hp_m}倍')
    elif hp_m == rec_m > 0:
        temp_text.append(f'HP和回复力{hp_m}倍')
        if atk_m > 0:
            temp_text.append(f'攻击力{atk_m}倍')
    elif hp_m == atk_m > 0:
        temp_text.append(f'HP和攻击力{hp_m}倍')
        if rec_m > 0:
            temp_text.append(f'回复力{rec_m}倍')
    elif atk_m == rec_m > 0:
        if hp_m > 0:
            temp_text.append(f'HP{hp_m}倍')
        temp_text.append(f'攻击力和回复力{atk_m}倍')
    else:
        if hp_m > 0:
            temp_text.append(f'HP{hp_m}倍')
        if atk_m > 0:
            temp_text.append(f'攻击力{atk_m}倍')
        if rec_m > 0:
            temp_text.append(f'回复力{rec_m}倍')

    return "、".join(temp_text)
