from .skill_common import *


# 打出指定combo时，所有宠物增加攻击力
def skill_type_101(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    atk_times = get_times(p[1])

    cond_req = p[0]

    result['desc_cn'].append(f'消除正好{cond_req}COMBO时，{get_pet_status_text(0, atk_times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    update_leader_buff(result, leader_buff)

    result['detail']['specific_combo_status'] = [cond_req]


# 打出指定combo以上时，所有宠物增加攻击力和回复力
def skill_type_103(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    times = get_times(p[3])

    status = [0, 0, 0]
    if p[1] > 0:
        status[p[1]] = times
    if p[2] > 0:
        status[p[2]] = times
    [hp_m, atk_m, rec_m] = status

    cond_req = p[0]

    result['desc_cn'].append(f'消除{cond_req}COMBO以上时，{get_pet_status_text(hp_m, atk_m, rec_m)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m
    leader_buff['rec'] = rec_m
    update_leader_buff(result, leader_buff)

    result['detail']['combo_status'] = [cond_req]


# 打出指定combo以上时，特定属性增加攻击力和回复力
def skill_type_104(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    times = get_times(p[4])

    status = [0, 0, 0]
    if p[2] > 0:
        status[p[2]] = times
    if p[3] > 0:
        status[p[3]] = times
    [hp_m, atk_m, rec_m] = status

    pet_category = convert_pet_category(p[1])
    cond_req = p[0]

    result['desc_cn'].append(f'消除{cond_req}COMBO以上时，{get_pet_category_text(pet_category)}宠物{get_pet_status_text(hp_m, atk_m, rec_m)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_m
    leader_buff['rec'] = rec_m
    update_leader_buff(result, leader_buff, pet_category)

    result['detail']['combo_status'] = [cond_req]


# 总HP减少，按属性提升伤害
def skill_type_107(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    hp_times = get_times(p[0])
    atk_times = get_times(p[2])

    if p[1] > 0:
        pet_category = convert_pet_category(p[1])

        result['desc_cn'].append(f'HP最大值变为{hp_times}%，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, 0)}')

        leader_buff = get_blank_leader_buff()
        leader_buff['hp'] = hp_times
        leader_buff['atk'] = atk_times
        update_leader_buff(result, leader_buff, pet_category)
    else:
        # 单纯减少HP的debuff
        result['desc_cn'].append(f'HP最大值变为{hp_times}%')

        leader_buff = get_blank_leader_buff()
        leader_buff['hp'] = hp_times
        update_leader_buff(result, leader_buff)


# 总HP减少，按类型提升伤害
def skill_type_108(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    hp_times = get_times(p[0])
    atk_times = get_times(p[2])

    if p[1] > 0:
        pet_category = convert_pet_category()
        pet_category[p[1] + 10] = 1

        result['desc_cn'].append(f'HP最大值变为{hp_times}%，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, 0)}')

        leader_buff = get_blank_leader_buff()
        leader_buff['hp'] = hp_times
        leader_buff['atk'] = atk_times
        update_leader_buff(result, leader_buff, pet_category)
    else:
        raise Exception('未处理分支')


# 两个属性提升攻击力
def skill_type_111(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 两个属性提升全属性
def skill_type_114(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[2])

    pet_category = convert_pet_category()
    pet_category[p[0]] = 1
    pet_category[p[1]] = 1

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(times, times, times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = times
    leader_buff['atk'] = times
    leader_buff['rec'] = times

    update_leader_buff(result, leader_buff, pet_category)


# 一次性消除指定个数以上的珠子时，提升攻击力
def skill_type_119(result, skill_id, skill_data):
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


# flag属性和类型分别提升三个属性
def skill_type_121(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    hp_times = get_times(p[2])
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])

    pet_category = convert_pet_category(p[0], p[1])

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times

    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以下时，按属性和类型强化攻击力和回复力
def skill_type_122(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])

    pet_category = convert_pet_category(p[1], p[2])

    result['desc_cn'].append(f'HP在{p[0]}%以下时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, rec_times)}')
    result['detail']['hp_low_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以上时，按属性和类型强化攻击力和回复力
def skill_type_123(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])

    pet_category = convert_pet_category(p[1], p[2])

    if p[0] == 100:
        result['desc_cn'].append(f'HP全满时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, rec_times)}')
    else:
        result['desc_cn'].append(f'HP在{p[0]}%以上时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, rec_times)}')
    result['detail']['hp_high_status'] = [p[0]]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)


# 按要求打出宝珠组合时，强化攻击力
def skill_type_124(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)

    # 触发宝珠
    cond_map = {
        'order': [],
        'orb': {},
        'all_one': True
    }
    for index in range(5):
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

    # 只用一种宝珠的场合
    cond_req = p[5]
    cond_max = len(cond_map['order'])
    atk_base = get_times(p[6])  # 最低倍率
    atk_pre_level = get_times(p[7])  # 每额外一层的倍率
    atk_max = get_times(atk_base + atk_pre_level * (cond_max - cond_req), 1)

    if len(cond_map['orb']) == 1:
        orb_id = cond_map['order'][0]
        if cond_max == cond_req:
            result['desc_cn'].append(f'消除{get_orb_text(orb_id)}{cond_max}COMBO以上时，{get_pet_status_text(0, atk_base, 0)}')
        else:
            result['desc_cn'].append(f'消除{get_orb_text(orb_id)}{cond_req}COMBO时，{get_pet_status_text(0, atk_base, 0)}，每多1COMBO额外增加{atk_pre_level}倍，最大{cond_max}COMBO时{atk_max}倍')
    elif cond_map['all_one']:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'{orb_array_text}同时攻击时，{get_pet_status_text(0, atk_base, 0)}')
        elif cond_max - cond_req == 1:
            # 目前好像没有这个
            result['desc_cn'].append(f'{orb_array_text}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, 0)}，{cond_max}种时{atk_max}倍')
        else:
            # 目前好像没有这个
            result['desc_cn'].append(f'{orb_array_text}中的{cond_req}种同时攻击时，{get_pet_status_text(0, atk_base, 0)}，每多1种额外增加{atk_pre_level}倍，最大{cond_max}种时{atk_max}倍')
    else:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'消除{orb_array_text}组合时，{get_pet_status_text(0, atk_base, 0)}')
        elif cond_max - cond_req == 1:
            result['desc_cn'].append(f'消除{orb_array_text}中的{cond_req}组时，{get_pet_status_text(0, atk_base, 0)}，{cond_max}组时{atk_max}倍')
        else:
            # 目前好像没有这个
            result['desc_cn'].append(f'消除{orb_array_text}中的{cond_req}组时，{get_pet_status_text(0, p[6], 0)}，每多1组额外增加{atk_pre_level}倍，最大{cond_max}组时{atk_max}倍')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = atk_max
    update_leader_buff(result, leader_buff)


# 队伍中有特定队员时提升
# TODO:额外处理
def skill_type_125(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    hp_times = get_times(p[5])
    atk_times = get_times(p[6])
    rec_times = get_times(p[7])

    result['desc_cn'].append(f'队伍中同时有以下宠物时，{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff)
    result['detail']['need_card'] = []
    for i in range(5):
        if p[i] > 0:
            result['detail']['need_card'].append(p[i])



# 按属性、类型被动强化三围和受到属性伤害减少
def skill_type_129(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)

    leader_buff = get_blank_leader_buff()
    pet_category = convert_pet_category(p[0], p[1])

    if p[0] + p[1] > 0:
        hp_m = get_times(p[2])  # HP
        atk_m = get_times(p[3])  # 攻击力
        rec_m = get_times(p[4])  # 回复力

        result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')

        leader_buff['hp'] = hp_m if hp_m > 0 else 1
        leader_buff['atk'] = atk_m if atk_m > 0 else 1
        leader_buff['rec'] = rec_m if rec_m > 0 else 1

    if p[5] > 0:
        enemy_category = convert_pet_category(p[5])
        result['desc_cn'].append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{p[6]}%')

        leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
        for ele_id in range(0, 5):
            if enemy_category[ele_id]:
                leader_buff['ele_d_rate'][ele_id] = 100 - p[6]

    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以下时，变化特定属性的攻击和回复力
def skill_type_130(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])
    d_rate = p[6]

    pet_category = convert_pet_category(p[1], p[2])
    leader_buff = get_blank_leader_buff()

    temp_text = [f'HP在{p[0]}%以下时']

    if atk_times + rec_times > 0:
        pet_category_text = get_pet_category_text(pet_category)
        if pet_category == '所有':
            temp_text.append(f'，{get_pet_status_text(0, atk_times, rec_times)}')
        else:
            temp_text.append(f'，{pet_category_text}宠物的{get_pet_status_text(0, atk_times, rec_times)}')
        result['detail']['hp_low_status'] = [p[0]]

    if d_rate > 0:
        enemy_category = convert_pet_category(p[5])
        enemy_category_text = get_pet_category_text(enemy_category)
        if enemy_category_text == '所有':
            temp_text.append(f'，受到的伤害减少{d_rate}%')
            leader_buff['d_rate'] = 100 - d_rate
        else:
            temp_text.append(f'，被{enemy_category_text}敌人攻击时，受到的伤害减少{d_rate}%')
            leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
            for ele_id in range(0, 5):
                if enemy_category[ele_id]:
                    leader_buff['ele_d_rate'][ele_id] = 100 - p[6]
    result['desc_cn'].append(''.join(temp_text))

    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)


# HP在百分比以上时，变化特定属性的攻击和回复力
def skill_type_131(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 7)
    atk_times = get_times(p[3])
    rec_times = get_times(p[4])
    d_rate = p[6]

    pet_category = convert_pet_category(p[1], p[2])
    leader_buff = get_blank_leader_buff()

    temp_text = [f'HP在{p[0]}%以上时']

    if atk_times + rec_times > 0:
        pet_category_text = get_pet_category_text(pet_category)
        if pet_category == '所有':
            temp_text.append(f'，{get_pet_status_text(0, atk_times, rec_times)}')
        else:
            temp_text.append(f'，{pet_category_text}宠物的{get_pet_status_text(0, atk_times, rec_times)}')
        result['detail']['hp_high_status'] = [p[0]]

    if d_rate > 0:
        enemy_category = convert_pet_category(p[5])
        enemy_category_text = get_pet_category_text(enemy_category)
        if enemy_category_text == '所有':
            temp_text.append(f'，受到的伤害减少{d_rate}%')
            leader_buff['d_rate'] = 100 - d_rate
        else:
            temp_text.append(f'，被{enemy_category_text}敌人攻击时，受到的伤害减少{d_rate}%')
            leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
            for ele_id in range(0, 5):
                if enemy_category[ele_id]:
                    leader_buff['ele_d_rate'][ele_id] = 100 - p[6]
    result['desc_cn'].append(''.join(temp_text))

    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff, pet_category)


# 使用技能时，提高属性和类型的攻击力和回复力
def skill_type_133(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    atk_times = get_times(p[2])
    rec_times = get_times(p[3])

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


# 根据属性，提升三围，可以指定2段，效果相乘
def skill_type_136(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    pet_category_1 = convert_pet_category(p[0])
    hp_times_1 = get_times(p[1])
    atk_times_1 = get_times(p[2])
    rec_times_1 = get_times(p[3])

    assert p[4] > 0
    pet_category_2 = convert_pet_category(p[4])
    hp_times_2 = get_times(p[5])
    atk_times_2 = get_times(p[6])
    rec_times_2 = get_times(p[7])

    result['desc_cn'].append(f'{get_pet_category_text(pet_category_1)}宠物{get_pet_status_text(hp_times_1, atk_times_1, rec_times_1)}，'
                             f'{get_pet_category_text(pet_category_2)}宠物{get_pet_status_text(hp_times_2, atk_times_2, rec_times_2)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = max(hp_times_1, hp_times_2, hp_times_1 * hp_times_2)
    leader_buff['atk'] = max(atk_times_1, atk_times_2, atk_times_1 * atk_times_2)
    leader_buff['rec'] = max(rec_times_1, rec_times_2, rec_times_1 * rec_times_2)
    update_leader_buff(result, leader_buff)


# 根据类型，提升三围，可以指定2段，效果相乘
def skill_type_137(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    pet_category_1 = convert_pet_category(type_flag=p[0])
    hp_times_1 = get_times(p[1])
    atk_times_1 = get_times(p[2])
    rec_times_1 = get_times(p[3])

    assert p[4] > 0
    pet_category_2 = convert_pet_category(type_flag=p[4])
    hp_times_2 = get_times(p[5])
    atk_times_2 = get_times(p[6])
    rec_times_2 = get_times(p[7])

    result['desc_cn'].append(f'{get_pet_category_text(pet_category_1)}宠物{get_pet_status_text(hp_times_1, atk_times_1, rec_times_1)}，'
                             f'{get_pet_category_text(pet_category_2)}宠物{get_pet_status_text(hp_times_2, atk_times_2, rec_times_2)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = max(hp_times_1, hp_times_2, hp_times_1 * hp_times_2)
    leader_buff['atk'] = max(atk_times_1, atk_times_2, atk_times_1 * atk_times_2)
    leader_buff['rec'] = max(rec_times_1, rec_times_2, rec_times_1 * rec_times_2)
    update_leader_buff(result, leader_buff)


# 根据HP百分比变化攻击力，可以分2段
def skill_type_139(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    times = [get_times(p[4]), get_times(p[7])]

    pet_category = convert_pet_category(p[0], p[1])

    # p[3]和p[6]是判断位，0为以上，1为以下
    if times[0] == times[1]:
        assert p[3] != p[6]
        hp_percent_a = p[2] if p[3] < p[6] else p[5]
        hp_percent_b = p[5] if p[3] < p[6] else p[2]
        result['desc_cn'].append(f'HP{"全满" if hp_percent_a == 100 else f"在{hp_percent_a}%以上"}或在{hp_percent_b}%以下时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, times[0], 0)}')
        result['detail']['hp_high_status'] = [hp_percent_a]
        result['detail']['hp_low_status'] = [hp_percent_b]
    else:
        for i, p_index in enumerate([3, 6]):
            hp_percent = p[p_index - 1]
            atk_times = times[i]
            if p[p_index] == 0:
                if hp_percent == 100:
                    result['desc_cn'].append(f'HP全满时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, 0)}')
                else:
                    result['desc_cn'].append(f'HP在{hp_percent}%以上时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, 0)}')
                result['detail']['hp_high_status'] = [hp_percent]
            elif p[p_index] == 1:
                result['desc_cn'].append(f'HP在{hp_percent}%以下时，{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(0, atk_times, 0)}')
                result['detail']['hp_low_status'] = [hp_percent]

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = max(times)
    update_leader_buff(result, leader_buff, pet_category)


# 当队长进副本时提升RANK经验
def skill_type_148(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 1)
    times = get_times(p[0])

    result['desc_cn'].append(f'作为队长进入地下城时，获得的RANK经验值{times}倍')
    result['detail']['bonus_rank_exp'] = [times]


# 包含强化宝珠5个消除的属性攻击力的X倍
def skill_type_150(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    times = get_times(p[1])

    result['desc_cn'].append(f'消除含有强化宝珠的5个宝珠时，该属性的{get_pet_status_text(0, times, 0)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['atk'] = times

    update_leader_buff(result, leader_buff)
