from .skill_common import *


# 按属性提升攻击力
def skill_type_11(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(p[1], 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 消除宝珠追打
def skill_type_12(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[0] = get_times(p[0])

    result['desc_cn'].append(f'消除宝珠的回合，对敌方全体进行追打，造成自身攻击力{p[0]}倍的伤害（会被防御力减免，最低为0）')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk_add'] = p[0]

    update_leader_buff(result, leader_buff)


# 消除宝珠回复
def skill_type_13(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[0] = get_times(p[0])

    result['desc_cn'].append(f'消除宝珠的回合，回复自身回复力{p[0]}倍的HP')

    leader_buff = get_blank_leader_buff()
    leader_buff['rec_add'] = p[0]

    update_leader_buff(result, leader_buff)


# 根性
def skill_type_14(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    result['desc_cn'].append(f'剩余生命值在{p[0]}%以上时，受到致死伤害，会以1HP生还')
    result['detail']['last_stand'] = [p[0], p[1]]


# 操作时间延长
def skill_type_15(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[0] = get_times(p[0])

    result['desc_cn'].append(f'宝珠操作时间延长{p[0]}秒')

    leader_buff = get_blank_leader_buff()
    leader_buff['time'] = p[0]

    update_leader_buff(result, leader_buff)


# 属性伤害减少
def skill_type_17(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    enemy_category = convert_pet_category()
    enemy_category[p[0]] = 1

    result['desc_cn'].append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{p[1]}%')
    leader_buff = get_blank_leader_buff()
    leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
    leader_buff['ele_d_rate'][p[0]] = 100 - p[1]

    update_leader_buff(result, leader_buff)


# 全伤害减少
def skill_type_16(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    result['desc_cn'].append(f'受到的所有伤害减少{p[0]}%')
    leader_buff = get_blank_leader_buff()
    leader_buff['d_rate'] = 100 - p[0]

    update_leader_buff(result, leader_buff)


# 按类型提升攻击力
def skill_type_22(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, p[1], 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升HP
def skill_type_23(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(p[1], 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升回复力
def skill_type_24(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, 0, p[1])}')

    leader_buff = get_blank_leader_buff()
    leader_buff['rec'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按属性提升攻击力和回复力
def skill_type_28(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, p[1], p[1])}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = p[1]
    leader_buff['rec'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按属性提升全属性
def skill_type_29(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(p[1], p[1], p[1])}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = p[1]
    leader_buff['atk'] = p[1]
    leader_buff['rec'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按双类型提升HP
def skill_type_30(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[2] = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(p[1], 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 按双类型提升攻击力
def skill_type_31(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[2] = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(p[1], 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = p[1]

    update_leader_buff(result, leader_buff, pet_category)


# 变化操作时的音效
def skill_type_33(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    result['desc_cn'].append(f'操作宝珠时发出太鼓的声音')


# 双属性减伤
def skill_type_36(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    leader_buff = get_blank_leader_buff()

    enemy_category = convert_pet_category()
    enemy_category[p[0]] = 1
    enemy_category[p[1]] = 1

    result['desc_cn'].append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{p[2]}%')

    leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
    for ele_id in range(0, 5):
        if enemy_category[ele_id]:
            leader_buff['ele_d_rate'][ele_id] = 100 - p[2]

    update_leader_buff(result, leader_buff)


# 反击
def skill_type_41(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    p[1] = get_times(p[1])

    if p[0] == 100:
        result['desc_cn'].append(f'受到伤害时进行反击，对敌方全体造成自身攻击力{p[1]}倍的{element(p[2])}伤害')
    else:
        result['desc_cn'].append(f'受到伤害时有{p[0]}%几率进行反击，对敌方全体造成自身攻击力{p[1]}倍的{element(p[2])}伤害')
    result['detail']['counter_attack'] = [p[0], p[1], p[2]]


# HP在百分比以上时，变化三围
def skill_type_44(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)

    status = [0, 0, 0]
    status[p[1]] = get_times(p[3])
    [hp_m, atk_m, rec_m] = status

    if p[0] == 100:
        result['desc_cn'].append(f'HP全满时，所有宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
        result['detail']['hp_max'] = [True]
    else:
        result['desc_cn'].append(f'HP在{p[0]}以上时，所有宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')
        result['detail']['hp_high'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_m if hp_m > 0 else 1
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff)
