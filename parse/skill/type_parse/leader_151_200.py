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
    result['detail']['cross_bonus'] = [True]


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

    result['detail']['cross_bonus'] = [True]
    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = cond_map[0]["ele_times"] * cond_map[0]["ele_times"]

    update_leader_buff(result, leader_buff)


# 打出指定combo以上时，所有宠物增加攻击力和回复力，可增强
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
    rec_per_level = atk_per_level
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
