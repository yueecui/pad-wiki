from .skill_common import *


# 按属性提升攻击力
def skill_type_11(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 消除宝珠追打
def skill_type_12(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[0])

    result['desc_cn'].append(f'消除宝珠的回合，对敌方全体进行追打，造成自身攻击力{times}倍的伤害（会被防御力减免，最低为0）')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk_add'] = times

    update_leader_buff(result, leader_buff)


# 消除宝珠回复
def skill_type_13(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[0])

    result['desc_cn'].append(f'消除宝珠的回合，回复自身回复力{times}倍的HP')

    leader_buff = get_blank_leader_buff()
    leader_buff['rec_add'] = times

    update_leader_buff(result, leader_buff)


# 根性
def skill_type_14(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    result['desc_cn'].append(f'剩余生命值在{p[0]}%以上时，受到致死伤害，会以1HP生还')
    result['detail']['last_stand'] = [p[0], p[1]]


# 操作时间延长
def skill_type_15(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    move_time = get_times(p[0])

    result['desc_cn'].append(f'宝珠操作时间延长{move_time}秒')

    leader_buff = get_blank_leader_buff()
    leader_buff['time'] = move_time

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
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升HP
def skill_type_23(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按类型提升回复力
def skill_type_24(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0] + 10] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, 0, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按属性提升攻击力和回复力
def skill_type_28(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按属性提升全属性
def skill_type_29(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按双类型提升HP
def skill_type_30(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按双类型提升攻击力
def skill_type_31(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

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


# HP在百分比以下时，一定几率减少伤害
def skill_type_38(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    leader_buff = get_blank_leader_buff()
    leader_buff['d_rate'] = 100 - p[2]

    assert p[1] == 100  # p[1]应该是几率，目前都是100
    if p[0] == 100:
        # 不知道为什么这个函数p[0]==100的时候也是全满，只有一例No.3390 - 神国の魔術神・オーディン
        result['desc_cn'].append(f'HP全满时，受到的伤害减少{p[2]}%')
        result['detail']['hp_high_status'] = [p[0]]
    else:
        result['desc_cn'].append(f'HP在{p[0]}%以下时，受到的伤害减少{p[2]}%')
        result['detail']['hp_low_status'] = [p[0]]

    update_leader_buff(result, leader_buff)


# HP在百分比以下时，变化三围
def skill_type_39(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    times = get_times(p[3])

    status = [0, 0, 0]
    if p[1] > 0:
        status[p[1]] = times
    if p[2] > 0:
        status[p[1]] = times
    [hp_m, atk_m, rec_m] = status

    assert p[0] < 100

    result['desc_cn'].append(f'HP在{p[0]}%以下时，{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_low_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff)


# 按双属性提升攻击力
def skill_type_40(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 反击
def skill_type_41(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    times = get_times(p[1])

    if p[0] == 100:
        result['desc_cn'].append(f'受到伤害时进行反击，对敌方全体造成自身攻击力{times}倍的{element(p[2])}伤害')
    else:
        result['desc_cn'].append(f'受到伤害时有{p[0]}%几率进行反击，对敌方全体造成自身攻击力{times}倍的{element(p[2])}伤害')
    result['detail']['counter_attack'] = [p[0], times, p[2]]


# HP在百分比以上时，一定几率减少伤害
def skill_type_43(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    leader_buff = get_blank_leader_buff()

    if p[0] == 100:
        if p[1] == 100:
            result['desc_cn'].append(f'HP全满时，受到的伤害减少{p[2]}%')
            leader_buff['d_rate'] = 100 - p[2]
        else:
            result['desc_cn'].append(f'HP全满时，有{p[1]}%几率减少受到的伤害{p[2]}%')
    elif p[0] == 1:
        if p[1] == 100:
            result['desc_cn'].append(f'HP在{p[0]}%以上时，受到的伤害减少{p[2]}%')
            leader_buff['d_rate'] = 100 - p[2]
        else:
            result['desc_cn'].append(f'HP在{p[0]}%以上时，有{p[1]}%几率减少受到的伤害{p[2]}%')
    else:
        if p[1] == 100:
            result['desc_cn'].append(f'受到的所有伤害减少{p[2]}%')
            leader_buff['d_rate'] = 100 - p[2]
        else:
            result['desc_cn'].append(f'有{p[1]}%几率减少受到的伤害{p[2]}%')
    update_leader_buff(result, leader_buff)


# HP在百分比以上时，变化攻击力和回复力
def skill_type_44(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    times = get_times(p[3])

    status = [0, 0, 0]
    if p[1] > 0:
        status[p[1]] = times
    if p[2] > 0:
        status[p[1]] = times
    [hp_m, atk_m, rec_m] = status

    if p[0] == 100:
        result['desc_cn'].append(f'HP全满时，{get_pet_status_text(hp_m, atk_m, rec_m)}')
    else:
        result['desc_cn'].append(f'HP在{p[0]}%以上时，{get_pet_status_text(hp_m, atk_m, rec_m)}')
    result['detail']['hp_high_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    update_leader_buff(result, leader_buff)


# 按属性提升HP和攻击力
def skill_type_45(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 按双属性提升HP
def skill_type_46(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 单属性提升HP
def skill_type_48(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, 0, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 单属性提升回复力
def skill_type_49(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, 0, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)
