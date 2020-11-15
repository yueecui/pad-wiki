from .skill_common import *


# 当队长进副本时提升金币
def skill_type_54(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 1)
    times = get_times(p[0])

    result['desc_cn'].append(f'作为队长进入地下城时，获得的金币{times}倍')
    result['detail']['bonus_coin'] = [times]


# 多色同时攻击提高攻击力
def skill_type_61(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)

    # 触发宝珠
    orb_array = bitmap_to_flag_array(p[0])

    cond_req = p[1]
    cond_count = sum(orb_array)
    atk_base = get_times(p[2])  # 最低倍率
    atk_pre_level = get_times(p[3])  # 每额外一层的倍率
    cond_req_max = cond_count if atk_pre_level > 0 else cond_req
    atk_max = get_times(atk_base + atk_pre_level * (cond_req_max - cond_req), 1)

    if cond_count == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}同时攻击时，{get_pet_status_text(0, atk_base, 0)}')
    elif cond_req_max - cond_req == 1:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, 0)}，{cond_req_max}种时{atk_max}倍')
    elif cond_req_max == cond_req:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种或以上同时攻击时，{get_pet_status_text(0, atk_base, 0)}')
    else:
        result['desc_cn'].append(f'{get_enable_orb_text(orb_array)}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, 0)}，每多1种额外增加{atk_pre_level}倍，最大{cond_req_max}种时{atk_max}倍')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    update_leader_buff(result, leader_buff)


# 按类型提升HP和攻击力
def skill_type_62(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升HP和回复力
def skill_type_63(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升攻击力和回复力
def skill_type_64(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升全属性
def skill_type_65(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按属性提升HP和回复力
def skill_type_67(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按1个类型和1个属性提升攻击力
def skill_type_69(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# COMBO数在X以上时，提升攻击力
def skill_type_66(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    times = get_times(p[1])

    result['desc_cn'].append(f'{p[0]}COMBO以上时，{get_pet_status_text(0, times, 0)}')
    result['detail']['combo_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times
    update_leader_buff(result, leader_buff)


# 按1个类型和1个属性提升攻击力和回复力
def skill_type_75(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 两个类型提升HP和攻击力
def skill_type_77(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 一个属性和一个类型提升HP和攻击力
def skill_type_73(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 一个属性和一个类型提升全属性
def skill_type_76(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 两个类型提升攻击力和回复力
def skill_type_79(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1
    pet_category[p[1] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以下时，变化特定属性的攻击和回复力
def skill_type_94(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    times = get_times(p[4])

    pet_category = convert_pet_category()
    pet_category[p[1]] = 1

    status = [0, 0, 0]
    if p[2] > 0:
        status[p[2]] = times
    if p[3] > 0:
        status[p[3]] = times
    [hp_m, atk_m, rec_m] = status

    assert p[0] < 100

    result['desc_cn'].append(f'HP在{p[0]}%以下时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_low_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以下时，变化特定类型的攻击和回复力
def skill_type_95(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    times = get_times(p[4])

    pet_category = convert_pet_category()
    pet_category[p[1] + 10] = 1

    status = [0, 0, 0]
    if p[2] > 0:
        status[p[2]] = times
    if p[3] > 0:
        status[p[3]] = times
    [hp_m, atk_m, rec_m] = status

    assert p[0] < 100

    result['desc_cn'].append(f'HP在{p[0]}%以下时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_low_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以上时，变化特定属性的攻击力和回复力
def skill_type_96(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    times = get_times(p[4])

    pet_category = convert_pet_category()
    pet_category[p[1]] = 1

    status = [0, 0, 0]
    if p[2] > 0:
        status[p[2]] = times
    if p[3] > 0:
        status[p[3]] = times
    [hp_m, atk_m, rec_m] = status

    if p[0] == 100:
        result['desc_cn'].append(f'HP全满时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    else:
        result['desc_cn'].append(f'HP在{p[0]}%以上时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_high_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以上时，变化特定TYPE的攻击力和回复力
def skill_type_97(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    times = get_times(p[4])

    pet_category = convert_pet_category()
    pet_category[p[1] + 10] = 1

    status = [0, 0, 0]
    if p[2] > 0:
        status[p[2]] = times
    if p[3] > 0:
        status[p[3]] = times
    [hp_m, atk_m, rec_m] = status

    if p[0] == 100:
        result['desc_cn'].append(f'HP全满时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    else:
        result['desc_cn'].append(f'HP在{p[0]}%以上时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_high_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff, pet_category)


# 打出指定combo以上时，增加攻击力
def skill_type_98(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    cond_req = p[0]
    cond_max = p[3]
    atk_times = get_times(p[1])
    atk_pre_combo = get_times(p[2])
    atk_max = get_times(atk_times + atk_pre_combo * (cond_max - cond_req), 1)

    if cond_max == cond_req:
        result['desc_cn'].append(f'消除{cond_max}COMBO以上时，{get_pet_status_text(0, atk_times, 0)}')
    else:
        result['desc_cn'].append(f'消除{cond_req}COMBO时，{get_pet_status_text(0, atk_times, 0)}，每+1COMBO额外{atk_pre_combo}倍，最大{cond_max}COMBO时{atk_max}倍')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    update_leader_buff(result, leader_buff)

    result['detail']['combo_status'] = [cond_req]


# 使用技能时，提高属攻击力和回复力
def skill_type_100(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    atk_times = get_times(p[2])
    rec_times = atk_times

    pet_category = convert_pet_category(p[0], p[1])
    pet_category_text = get_pet_category_text(pet_category)

    if pet_category_text == '所有':
        result['desc_cn'].append(f'使用技能时，{get_pet_status_text(0, atk_times, rec_times)}')
    else:
        result['desc_cn'].append(f'使用技能时，{pet_category_text}宠物的{get_pet_status_text(0, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times

    update_leader_buff(result, leader_buff, pet_category)


