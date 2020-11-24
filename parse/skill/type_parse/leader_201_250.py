from .skill_common import *


# 按要求打出宝珠组合时，进行追打
def skill_type_201(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)

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
    flat_add = p[5]

    # 只用一种宝珠的场合
    if len(cond_map['orb']) == 1:
        orb_id = cond_map['order'][0]
        result['desc_cn'].append(f'消除{get_orb_text(orb_id)}{cond_req}COMBO以上时进行追打，造成{flat_add}点固定伤害')
    elif cond_map['all_one']:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'{orb_array_text}同时攻击时进行追打，造成{flat_add}点固定伤害')
        elif cond_req == 1:
            result['desc_cn'].append(f'{orb_array_text}中任意1种攻击时进行追打，造成{flat_add}点固定伤害')
        else:
            raise Exception('未处理的分支')
            # result['desc_cn'].append(f'{orb_array_text}中的{cond_req}种同时攻击时进行追打，造成{flat_add}点固定伤害')
    else:
        raise Exception('未处理的分支')

    leader_buff = get_blank_leader_buff()
    leader_buff['flat_add'] = flat_add
    update_leader_buff(result, leader_buff)


# 队伍全部为特定进化类型时，提升全属性
def skill_type_203(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    evo_type = p[0]
    hp_times = get_times(p[1])
    atk_times = get_times(p[2])
    rec_times = get_times(p[3])

    if evo_type == 0:
        evo_type_text = '点阵进化'
    elif evo_type == 2:
        evo_type_text = '转生、超转生进化'
    else:
        raise Exception('未预料的进化类型')

    result['desc_cn'].append(f'队伍完全由{evo_type_text}宠物组成时，{get_pet_status_text(hp_times, atk_times, rec_times)}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_times
    leader_buff['atk'] = atk_times
    leader_buff['rec'] = rec_times
    update_leader_buff(result, leader_buff)

    result['detail']['evo_bonus'] = [evo_type]


# 按要求的珠子打出combo时，增加combo数
def skill_type_206(result, skill_id, skill_data):
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
    add_combo = p[6]  # 附加combo

    if len(cond_map['orb']) == 1:
        orb_id = cond_map['order'][0]
        if cond_max == cond_req:
            result['desc_cn'].append(f'消除{get_orb_text(orb_id)}{cond_max}COMBO以上时，额外加算{add_combo}COMBO')
        else:
            raise Exception('未处理的分支')
    elif cond_map['all_one']:
        orb_array_text = ''.join([get_orb_text(orb_id) for orb_id in cond_map['order']])
        if cond_max == cond_req:
            result['desc_cn'].append(f'{orb_array_text}同时攻击时，额外加算{add_combo}COMBO')
        else:
            raise Exception('未处理的分支')
    else:
        raise Exception('未处理的分支')

    leader_buff = get_blank_leader_buff()
    leader_buff['add_combo'] = add_combo
    update_leader_buff(result, leader_buff)


# 消除回复十字时提升COMBO
def skill_type_209(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 1)
    add_combo = p[0]

    result['desc_cn'].append(f'以十字形式消除5个{get_orb_text(5)}时，额外加算{add_combo}COMBO')
    result['detail']['cross_bonus'] = [True]
    leader_buff = get_blank_leader_buff()
    leader_buff['add_combo'] = add_combo
    update_leader_buff(result, leader_buff)


# 消除十字提升COMBO
def skill_type_210(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    orb_array = bitmap_to_flag_array(p[0])
    add_combo = p[2]

    result['desc_cn'].append(f'以十字形式消除5个{get_enable_orb_text(orb_array)}时，额外加算{add_combo}COMBO')
    result['detail']['cross_bonus'] = [True]
    leader_buff = get_blank_leader_buff()
    leader_buff['add_combo'] = add_combo
    update_leader_buff(result, leader_buff)
