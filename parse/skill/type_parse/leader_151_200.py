from .skill_common import *


# 消除回复十字时提升攻击力、回复力和减伤
def skill_type_151(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    atk_times = get_times(p[0])
    rec_times = get_times(p[1])
    d_rate = p[2]

    result['desc_cn'].append(
            f'以十字形式消除5个{get_orb_text(5)}时，{get_pet_status_text(0, atk_times, rec_times)}'
            f'，受到的伤害减少{d_rate}%' if d_rate > 0 else "")

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    leader_buff['d_rate'] = 100 - d_rate

    update_leader_buff(result, leader_buff)
    result['detail']['cross_bonus'] = True


# 多人联机时提升全属性
def skill_type_155(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    # 参数0和参数1可能是属性和类型，但目前全是31和0
    pet_category = convert_pet_category(p[0], p[1])
    hp_times = get_times(p[2])
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])

    result['desc_cn'].append(f'联机时，{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff)
    result['detail']['multi_bonus'] = True


# 消除十字提升伤害
def skill_type_157(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    cond_map = []
    times_record = 0
    same_times = True
    orb_array = bitmap_to_flag_array(p[0])

    for index in [0, 2, 4]:
        ele_id = p[index]
        ele_times = get_times(p[index+1])
        if ele_times > 0:
            cond_map.append({
                'ele_id': ele_id,
                'ele_times': ele_times,
            })
            orb_array[ele_id] = 1
            if times_record == 0:
                times_record = ele_times
            elif times_record != ele_times:
                same_times = False

    if same_times:
        result['desc_cn'].append(
            f'以十字形式消除5个{get_enable_orb_text(orb_array)}时，{get_pet_status_text(0, cond_map[0]["ele_times"], 0)}，消除多组时倍率相乘')
    else:
        raise Exception('未处理的情况')

    result['detail']['cross_bonus'] = True
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = cond_map[0]["ele_times"] * cond_map[0]["ele_times"]

    update_leader_buff(result, leader_buff)


# 提升最低消除的数量，并按属性和类型提升全属性
def skill_type_158(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    min_remove = p[0]
    hp_times = get_times(p[3])  # HP
    atk_times = get_times(p[4])  # 攻击力
    rec_times = get_times(p[5])  # 回复力
    pet_category = convert_pet_category(p[1], p[2])

    # enemy_category = convert_pet_category(p[5])
    # d_rate = p[6]

    temp_text = []
    if pet_category['total'] > 0:
        temp_text.append(f'{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_times, atk_times, rec_times)}')
    # if enemy_category['total'] > 0:
    #     if get_pet_category_text(enemy_category) == '所有':
    #         temp_text.append(f'受到的所有伤害减少{d_rate}%')
    #     else:
    #         temp_text.append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{d_rate}%')

    result['desc_cn'].append('，'.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    # leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff, pet_category)
    result['detail']['min_remove'] = [min_remove]


# 一次性消除指定个数以上的珠子时，提升攻击力，可以增强
def skill_type_159(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    atk_base = get_times(p[2])
    atk_per_orb = get_times(p[3])
    cond_req = p[1]
    cond_max = p[4]
    has_extra = bool((cond_max > cond_req) and atk_per_orb > 0)
    atk_max = get_times((atk_base + atk_per_orb * (cond_max - cond_req)) if has_extra else atk_base, 1)

    orb_array = bitmap_to_flag_array(p[0])

    temp_text = []
    if len(orb_array) == sum(orb_array):
        if has_extra:
            temp_text.append(f'一次性消除任意一种宝珠{cond_req}个时，{get_pet_status_text(0, atk_base, 0)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{atk_max}倍")
            else:
                temp_text.append(f"，每多1个额外{atk_per_orb}倍，最大{cond_max}个时{atk_max}倍")
        else:
            temp_text.append(f'一次性消除任意一种宝珠{cond_req}个以上时，{get_pet_status_text(0, atk_base, 0)}')
    elif sum(orb_array) == 1:
        if has_extra:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个时，{get_pet_status_text(0, atk_base, 0)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{atk_max}倍")
            else:
                temp_text.append(f"，每多1个额外{atk_per_orb}倍，最大{cond_max}个时{atk_max}倍")
        else:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个以上时，{get_pet_status_text(0, atk_base, 0)}')
    else:
        if has_extra:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个时，{get_pet_status_text(0, atk_base, 0)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{atk_max}倍")
            else:
                temp_text.append(f"，每多1个额外{atk_per_orb}倍，最大{cond_max}个时{atk_max}倍")
        else:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个以上时，{get_pet_status_text(0, atk_base, 0)}')

    result['desc_cn'].append(''.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    update_leader_buff(result, leader_buff)


# 7x6面板
def skill_type_162(result, skill_id, skill_data):
    # p = list(skill_data[skill_id].params)
    result['detail']['big_board'] = True


# 不计掉落宝珠，并按属性和类型提升全属性
def skill_type_163(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)
    hp_times = get_times(p[2])  # HP
    atk_times = get_times(p[3])  # 攻击力
    rec_times = get_times(p[4])  # 回复力
    pet_category = convert_pet_category(p[0], p[1])

    enemy_category = convert_pet_category(p[5])
    d_rate = p[6]

    temp_text = []
    if pet_category['total'] > 0:
        temp_text.append(f'{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_times, atk_times, rec_times)}')
    if enemy_category['total'] > 0:
        if get_pet_category_text(enemy_category) == '所有':
            temp_text.append(f'受到的所有伤害减少{d_rate}%')
        else:
            temp_text.append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{d_rate}%')

    result['desc_cn'].append('，'.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff, pet_category)
    result['detail']['disable_drop'] = True


# 打出宝珠组合时，所有宠物增加攻击力和回复力，可增强
def skill_type_164(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)

    # 触发宝珠
    cond_map = {
        'order': [],
        'orb': {},
        'all_one': True
    }
    for index in range(4):
        if p[index] == 0:
            continue
        orb_array = bitmap_to_flag_array(p[index])
        assert sum(orb_array) == 1  # 目前所有条件都是1个珠子，出问题再改
        orb_id = orb_array.index(1)
        cond_map['order'].append(orb_id)
        if orb_id not in cond_map['orb']:
            cond_map['orb'][orb_id] = 1
        else:
            cond_map['orb'][orb_id] += 1
            cond_map['all_one'] = False

    cond_req = p[4]
    cond_max = len(cond_map['order'])
    atk_times = get_times(p[5])
    rec_times = get_times(p[6])
    atk_per_level = get_times(p[7])
    # rec_per_level = atk_per_level
    atk_max = get_times(atk_times + (cond_max - cond_req) * atk_per_level, 1)
    rec_max = get_times(atk_times + (cond_max - cond_req) * atk_per_level, 1)

    temp_text = []
    if len(cond_map['orb']) == 1:
        orb_id = cond_map['order'][0]
        temp_text.append(f'消除{get_orb_text(orb_id)}{cond_req}COMBO{"以上" if cond_req == cond_max else ""}时，{get_pet_status_text(0, atk_times, rec_times)}')
        if cond_max - cond_req == 1:
            temp_text.append(f"，{cond_max}COMBO时{get_pet_status_text(0, atk_max, rec_max)}")
        else:
            temp_text.append(f"，每多1个额外{atk_per_level}倍，最大{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
    elif cond_map['all_one']:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'{orb_array_text}同时攻击时，{get_pet_status_text(0, atk_times, rec_times)}')
        else:
            raise Exception('未处理的分支')
    else:
        raise Exception('未处理的分支')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    leader_buff['rec'] = rec_max
    update_leader_buff(result, leader_buff)


# 多色同时攻击提高攻击力和回复力
def skill_type_165(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)

    # 触发宝珠
    orb_array = bitmap_to_flag_array(p[0])

    cond_req = p[1]
    cond_count = sum(orb_array)
    atk_base = get_times(p[2])  # 最低倍率
    rec_base = get_times(p[3])  # 最低倍率
    atk_pre_level = get_times(p[4])  # 每额外一层的倍率
    rec_pre_level = get_times(p[5])  # 每额外一层的倍率
    cond_req_max = p[1] + p[6]
    atk_max = get_times(atk_base + atk_pre_level * (cond_req_max - cond_req), 1)
    rec_max = get_times(rec_base + rec_pre_level * (cond_req_max - cond_req), 1)

    if cond_count == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}同时攻击时，{get_pet_status_text(0, atk_base, rec_base)}')
    elif cond_req_max - cond_req == 1:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, rec_base)}，{cond_req_max}种时{get_pet_status_text(0, atk_max, rec_max)}')
    elif cond_req_max == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种或以上同时攻击时，{get_pet_status_text(0, atk_base, rec_base)}')
    else:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, rec_base)}，每多1种额外增加{get_pet_status_text(0, atk_pre_level, rec_pre_level)}，最大{cond_req_max}种时{get_pet_status_text(0, atk_max, rec_max)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    leader_buff['rec'] = rec_max
    update_leader_buff(result, leader_buff)


# 指定combo以上提高攻击力和回复力，可增强
def skill_type_166(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)

    # 触发宝珠
    cond_req = p[0]
    atk_base = get_times(p[1])  # 最低倍率
    rec_base = get_times(p[2])  # 最低倍率
    atk_pre_level = get_times(p[3])  # 每额外一层的倍率
    rec_pre_level = get_times(p[4])  # 每额外一层的倍率
    cond_req_max = p[5]
    atk_max = get_times(atk_base + atk_pre_level * (cond_req_max - cond_req), 1)
    rec_max = get_times(rec_base + rec_pre_level * (cond_req_max - cond_req), 1)

    if cond_req_max == cond_req:
        result['desc_cn'].append(f'消除{cond_req}COMBO以上时，{get_pet_status_text(0, atk_base, rec_base)}')
    elif cond_req_max - cond_req == 1:
        result['desc_cn'].append(f'消除{cond_req}COMBO时，{get_pet_status_text(0, atk_base, rec_base)}，{cond_req_max}COMBO时{get_pet_status_text(0, atk_max, rec_max)}')
    else:
        result['desc_cn'].append(f'消除{cond_req}COMBO时，{get_pet_status_text(0, atk_base, rec_base)}，每+1COMBO增加{get_pet_status_text(0, atk_pre_level, rec_pre_level)}，最大{cond_req_max}COMBO时{get_pet_status_text(0, atk_max, rec_max)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    leader_buff['rec'] = rec_max
    update_leader_buff(result, leader_buff)


# 指定颜色中，任意一种消除X个以上，提高攻击力和回复力
def skill_type_167(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)

    # 触发宝珠
    orb_array = bitmap_to_flag_array(p[0])

    cond_req = p[1]
    cond_count = sum(orb_array)
    atk_base = get_times(p[2])  # 最低倍率
    rec_base = get_times(p[3])  # 最低倍率
    atk_pre_level = get_times(p[4])  # 每额外一层的倍率
    rec_pre_level = get_times(p[5])  # 每额外一层的倍率
    cond_max = p[6]
    atk_max = get_times(atk_base + atk_pre_level * (cond_max - cond_req), 1)
    rec_max = get_times(rec_base + rec_pre_level * (cond_max - cond_req), 1)
    has_extra = bool((cond_max > cond_req) and (atk_pre_level > 0 or rec_pre_level > 0))

    temp_text = []
    if len(orb_array) == sum(orb_array):
        if has_extra:
            temp_text.append(f'一次性消除任意一种宝珠{cond_req}个时，{get_pet_status_text(0, atk_base, rec_base)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
            else:
                temp_text.append(f"，每多1个额外{get_pet_status_text(0, atk_pre_level, rec_pre_level)}，最大{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
        else:
            temp_text.append(f'一次性消除任意一种宝珠{cond_req}个以上时，{get_pet_status_text(0, atk_base, rec_base)}')
    elif sum(orb_array) == 1:
        if has_extra:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个时，{get_pet_status_text(0, atk_base, rec_base)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
            else:
                temp_text.append(f"，每多1个额外{get_pet_status_text(0, atk_pre_level, rec_pre_level)}，最大{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
        else:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个以上时，{get_pet_status_text(0, atk_base, rec_base)}')
    else:
        if has_extra:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个时，{get_pet_status_text(0, atk_base, rec_base)}')
            if cond_max - cond_req == 1:
                temp_text.append(f"，{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
            else:
                temp_text.append(f"，每多1个额外{get_pet_status_text(0, atk_pre_level, rec_pre_level)}，最大{cond_max}个时{get_pet_status_text(0, atk_max, rec_max)}")
        else:
            temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个以上时，{get_pet_status_text(0, atk_base, rec_base)}')

    result['desc_cn'].append(''.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    leader_buff['rec'] = rec_max
    update_leader_buff(result, leader_buff)


# 打出指定combo以上时，增加攻击力和减伤
def skill_type_169(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)

    cond_req = p[0]
    atk_times = get_times(p[1])
    d_rate = p[2]

    result['desc_cn'].append(f'消除{cond_req}COMBO以上时，{get_pet_status_text(0, atk_times, 0)}'
                             f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff)

    result['detail']['combo_status'] = [cond_req]


# 多色同时攻击提高攻击力和减伤
def skill_type_170(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    # 触发宝珠
    orb_array = bitmap_to_flag_array(p[0])

    cond_req = p[1]
    cond_count = sum(orb_array)
    atk_times = get_times(p[2])  # 攻击倍率
    d_rate = p[3]  # 减伤率

    if cond_count == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}同时攻击时，{get_pet_status_text(0, atk_times, 0)}'
                                 f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')
    else:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_times, 0)}'
                                 f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff)


# 按要求打出宝珠组合时，提升攻击力和减伤
def skill_type_171(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)

    # 触发宝珠
    cond_map = {
        'order': [],
        'orb': {},
        'all_one': True
    }
    for index in range(4):
        if p[index] == 0:
            continue
        orb_array = bitmap_to_flag_array(p[index])
        assert sum(orb_array) == 1  # 目前所有条件都是1个珠子，出问题再改
        orb_id = orb_array.index(1)
        cond_map['order'].append(orb_id)
        if orb_id not in cond_map['orb']:
            cond_map['orb'][orb_id] = 1
        else:
            cond_map['orb'][orb_id] += 1
            cond_map['all_one'] = False

    cond_req = p[4]
    cond_max = len(cond_map['order'])
    atk_times = get_times(p[5])
    d_rate = p[6]

    # 只用一种宝珠的场合
    if len(cond_map['orb']) == 1:
        orb_id = cond_map['order'][0]
        result['desc_cn'].append(f'消除{get_orb_text(orb_id)}{cond_req}COMBO以上时，{get_pet_status_text(0, atk_times, 0)}'
                                 f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')
    elif cond_map['all_one']:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'{orb_array_text}同时攻击时，{get_pet_status_text(0, atk_times, 0)}'
                                     f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')
        else:
            if cond_req == 1:
                result['desc_cn'].append(f'消除{orb_array_text}中任意1种时，{get_pet_status_text(0, atk_times, 0)}'
                                         f'{f"，受到的伤害减少{d_rate}%" if d_rate > 0 else ""}')
            else:
                raise Exception('未处理的分支')
            # result['desc_cn'].append(f'{orb_array_text}中的{cond_req}种同时攻击时进行追打，造成{flat_add}点固定伤害')
    else:
        raise Exception('未处理的分支')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff)


# 特定系列队员编成时，提升全属性
def skill_type_175(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    hp_times = get_times(p[3])  # HP
    atk_times = get_times(p[4])  # 攻击力
    rec_times = get_times(p[5])  # 回复力

    pet_kind = p[0]

    # 文本交给lua处理
    result['desc_cn'].append(f'队员编成均为<PetKind:{pet_kind}>时，{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff)
    result['detail']['kind_bonus'] = [pet_kind]


# 不计掉落宝珠，并按属性和类型提升全属性，并且转珠后剩余的宝珠数量越少提升攻击力越多
def skill_type_177(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    hp_times = get_times(p[2])  # HP
    atk_times = get_times(p[3])  # 攻击力
    rec_times = get_times(p[4])  # 回复力
    pet_category = convert_pet_category(p[0], p[1])

    remain_orb = p[5]
    remain_atk_times = get_times(p[6])
    remain_atk_times_pre = get_times(p[7])
    remain_atk_times_max = get_times(remain_atk_times + remain_atk_times_pre * remain_orb, 1)

    temp_text = []
    if pet_category['total'] > 0:
        temp_text.append(f'{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_times, atk_times, rec_times)}')
    if remain_orb > 0 and remain_atk_times > 0:
        if remain_atk_times_pre > 0:
            temp_text.append(f'消除宝珠后剩余宝珠数量为{remain_orb}时{get_pet_status_text(0, remain_atk_times, 0)}，'
                             f'每少1个额外{remain_atk_times_pre}倍，全部消除时{get_pet_status_text(0, remain_atk_times_max, 0)}')
        else:
            temp_text.append(f'消除宝珠后剩余宝珠数量为{remain_orb}个或更少时，{get_pet_status_text(0, remain_atk_times, 0)}')

    result['desc_cn'].append('，'.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times + remain_atk_times_max
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)
    result['detail']['disable_drop'] = True
    result['detail']['remain_orb'] = True


# 固定操作时间，按属性和类型提升全属性
def skill_type_178(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    hp_times = get_times(p[3])  # HP
    atk_times = get_times(p[4])  # 攻击力
    rec_times = get_times(p[5])  # 回复力

    pet_category = convert_pet_category(p[1], p[2])

    flat_time = p[0]

    # 文本交给lua处理
    if pet_category['total'] > 0:
        result['desc_cn'].append(f'{get_pet_category_text(pet_category)}的{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)
    result['detail']['flat_time'] = [flat_time]


# 一次性消除指定个数以上的珠子时，提升攻击力和减伤
def skill_type_182(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    atk_times = get_times(p[2])

    orb_array = bitmap_to_flag_array(p[0])

    if len(orb_array) == sum(orb_array):
        result['desc_cn'].append(
            f'一次性消除任意一种宝珠{p[1]}个以上时，{get_pet_status_text(0, atk_times, 0)}'
            f'{f"，受到的伤害减少{p[3]}%" if p[3] > 0 else ""}')
    elif sum(orb_array) == 1:
        result['desc_cn'].append(
            f'一次性消除{get_enable_orb_text(orb_array)}{p[1]}个以上时，{get_pet_status_text(0, atk_times, 0)}'
            f'{f"，受到的伤害减少{p[3]}%" if p[3] > 0 else ""}')
    else:
        result['desc_cn'].append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{p[1]}个以上时，{get_pet_status_text(0, atk_times, 0)}'
                                 f'{f"，受到的伤害减少{p[3]}%" if p[3] > 0 else ""}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['d_rate'] = 100 - p[3]

    update_leader_buff(result, leader_buff)


# 根据HP百分比以上变化攻击力和减伤，HP百分比以下变化攻击力和回复力
def skill_type_183(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    hp_percent_a = p[2]
    atk_times_a = get_times(p[3])
    d_rate = p[4]
    hp_percent_b = p[5]
    atk_times_b = get_times(p[6])
    rec_times_b = get_times(p[7])

    pet_category = convert_pet_category(p[0], p[1])
    pet_category_text = get_pet_category_text(pet_category)

    # HP以上
    temp_text = []
    if hp_percent_a > 0:
        temp_text.append(f'HP{"全满" if hp_percent_a == 100 else f"在{hp_percent_a}%以上"}')
        if atk_times_a > 0:
            if pet_category_text == '所有':
                temp_text.append(f'，{get_pet_status_text(0, atk_times_a, 0)}')
            else:
                temp_text.append(f'，{pet_category_text}宠物的{get_pet_status_text(0, atk_times_a, 0)}')
        if d_rate > 0:
            temp_text.append(f'，受到的伤害减少{d_rate}%')
        result['detail']['hp_high_status'] = [hp_percent_a]
        result['desc_cn'].append(''.join(temp_text))
    # HP以下
    temp_text = []
    if hp_percent_b > 0:
        temp_text.append(f'HP在{hp_percent_b}%以下时')
        if pet_category_text == '所有':
            temp_text.append(f'，{get_pet_status_text(0, atk_times_b, rec_times_b)}')
        else:
            temp_text.append(f'，{pet_category_text}宠物的{get_pet_status_text(0, atk_times_b, rec_times_b)}')
        result['detail']['hp_low_status'] = [hp_percent_b]
        result['desc_cn'].append(''.join(temp_text))

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = max(atk_times_a, atk_times_b)
    leader_buff['d_rate'] = 100 - d_rate
    leader_buff['rec'] = rec_times_b
    update_leader_buff(result, leader_buff, pet_category)


# 按属性、类型被动强化三围和移动时间
def skill_type_185(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    time_m = get_times(p[0])  # 移动时间
    hp_m = get_times(p[3])  # HP
    atk_m = get_times(p[4])  # 攻击力
    rec_m = get_times(p[5])  # 回复力

    pet_category = convert_pet_category(p[1], p[2])

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}'
                             f'{f"。宝珠操作时间延长{time_m}秒" if time_m > 0 else ""}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_m if hp_m > 0 else 1
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    leader_buff['time'] = time_m
    update_leader_buff(result, leader_buff, pet_category)


# 7x6面板，并按属性和类型提升全属性
def skill_type_186(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)
    hp_times = get_times(p[2])  # HP
    atk_times = get_times(p[3])  # 攻击力
    rec_times = get_times(p[4])  # 回复力
    pet_category = convert_pet_category(p[0], p[1])

    enemy_category = convert_pet_category(p[5])
    d_rate = p[6]

    temp_text = []
    if pet_category['total'] > 0:
        temp_text.append(f'{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_times, atk_times, rec_times)}')
    if enemy_category['total'] > 0:
        if get_pet_category_text(enemy_category) == '所有':
            temp_text.append(f'受到的所有伤害减少{d_rate}%')
        else:
            temp_text.append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{d_rate}%')

    result['desc_cn'].append('，'.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    leader_buff['d_rate'] = 100 - d_rate
    update_leader_buff(result, leader_buff, pet_category)
    result['detail']['big_board'] = True


# 指定宝珠一次性消除X个以上时，增加攻击力和COMBO
def skill_type_192(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    orb_array = bitmap_to_flag_array(p[0])
    cond_req = p[1]
    atk_times = get_times(p[2])
    add_combo = p[3]

    temp_text = []
    if len(orb_array) == sum(orb_array):
        temp_text.append(f'一次性消除任意一种宝珠{cond_req}个时')
    elif sum(orb_array) == 1:
        temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个时')
    else:
        temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个时')

    if atk_times > 0:
        temp_text.append(f'，{get_pet_status_text(0, atk_times, 0)}')
    if add_combo > 0:
        temp_text.append(f'，额外加算{add_combo}COMBO')

    result['desc_cn'].append(''.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['add_combo'] = add_combo
    update_leader_buff(result, leader_buff)


# L型消除指定宝珠时，提升攻击力、回复力、减伤
def skill_type_193(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    orb_array = bitmap_to_flag_array(p[0])
    atk_times = get_times(p[1])
    rec_times = get_times(p[2])
    d_rate = p[3]

    if len(orb_array) == sum(orb_array):
        result['desc_cn'].append(
            f'以L形消除5个宝珠时，{get_pet_status_text(0, atk_times, rec_times)}'
            f'，受到的伤害减少{d_rate}%' if d_rate > 0 else "")
    else:
        result['desc_cn'].append(
                f'以L形消除5个{get_enable_orb_text(orb_array)}时，{get_pet_status_text(0, atk_times, rec_times)}'
                f'，受到的伤害减少{d_rate}%' if d_rate > 0 else "")

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    leader_buff['d_rate'] = 100 - d_rate

    update_leader_buff(result, leader_buff)
    result['detail']['l_bonus'] = True


# 指定宝珠同时攻击时，增加攻击力和COMBO
def skill_type_194(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    orb_array = bitmap_to_flag_array(p[0])
    cond_req = p[1]
    atk_times = get_times(p[2])
    add_combo = p[3]

    temp_text = []
    if sum(orb_array) == cond_req:
        temp_text.append(f'{get_enable_orb_text(orb_array)}同时攻击时')
    else:
        temp_text.append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时')
    if atk_times > 0:
        temp_text.append(f'，{get_pet_status_text(0, atk_times, 0)}')
    if add_combo > 0:
        temp_text.append(f'，额外加算{add_combo}COMBO')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['add_combo'] = add_combo
    update_leader_buff(result, leader_buff)


# 消除十字提升COMBO
def skill_type_197(result, skill_id, skill_data):
    result['desc_cn'].append(f'毒伤害无效')
    result['detail']['immunity_poison'] = True


# 回复宝珠回复量达标时，提升攻击力，减伤，回复觉醒无效
def skill_type_198(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    cond_req = p[0]
    atk_times = get_times(p[1])
    d_rate = p[2]
    seal_recovery = p[3]

    temp_text = [f'{get_orb_text(5)}产生的回复量大于{cond_req}时']
    if atk_times > 0:
        temp_text.append(f'{get_pet_status_text(0, atk_times, 0)}')
    if d_rate > 0:
        temp_text.append(f'受到的伤害减少{d_rate}%')
    if seal_recovery == 9999:
        temp_text.append(f'觉醒无效状态全回复')
    elif seal_recovery > 0:
        temp_text.append(f'觉醒无效状态回复{seal_recovery}回合')

    result['desc_cn'].append('，'.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['d_rate'] = d_rate
    update_leader_buff(result, leader_buff)
    if seal_recovery > 0:
        result['detail']['seal_recovery'] = [seal_recovery]


# 若干色同时攻击时
def skill_type_199(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    orb_array = bitmap_to_flag_array(p[0])
    cond_req = p[1]
    cond_req_max = sum(orb_array)
    flat_add = p[2]

    temp_text = []
    if cond_req_max == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}同时攻击时进行追打，造成{flat_add}点固定伤害')
    else:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时进行追打，造成{flat_add}点固定伤害')

    result['desc_cn'].append(''.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['flat_add'] = flat_add
    update_leader_buff(result, leader_buff)


# 一次性消除指定属性的指定个数以上的珠子时，进行追打
def skill_type_200(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    orb_array = bitmap_to_flag_array(p[0])
    cond_req = p[1]
    flat_add = p[2]

    temp_text = []
    if len(orb_array) == sum(orb_array):
        temp_text.append(f'一次性消除任意一种宝珠{cond_req}个以上时进行追打，造成{flat_add}点固定伤害')
    elif sum(orb_array) == 1:
        temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}{cond_req}个以上时进行追打，造成{flat_add}点固定伤害')
    else:
        temp_text.append(f'一次性消除{get_enable_orb_text(orb_array)}中任意一种{cond_req}个以上时进行追打，造成{flat_add}点固定伤害')

    result['desc_cn'].append(''.join(temp_text))
    leader_buff = get_blank_leader_buff()
    leader_buff['flat_add'] = flat_add
    update_leader_buff(result, leader_buff)
