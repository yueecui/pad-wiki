from .skill_common import *


# 背水一击
def skill_type_110(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    p[2] = get_times(p[2])
    p[3] = get_times(p[3])
    if p[0] == 0:
        result['desc_cn'].append(f'根据当前HP对敌方全体造成{element(p[1])}伤害（100%HP时为自身攻击力的{p[2]}倍，1HP时为自身攻击力的{p[3]}倍）')
        result['detail']['ele_damage_all'] = [p[1], p[3], p[2]]
    elif p[0] == 1:
        result['desc_cn'].append(f'根据当前HP对敌方1体造成{element(p[1])}伤害（100%HP时为自身攻击力的{p[2]}倍，1HP时为自身攻击力的{p[3]}倍）')
        result['detail']['self_ele_damage_single'] = [p[1], p[3], p[2]]
    else:
        raise Exception(f'意料外的参数：skill_type_110：p[0]=={p[0]}')


# 倍率特定属性单体攻击技能+吸血
def skill_type_115(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'对敌方1体造成自身攻击力{p[0]}倍的{element(p[0])}属性伤害，并回复伤害{p[1]}%的HP')
    result['detail']['ele_damage_single'] = [10, p[0], 0]
    result['detail']['absorb_heal'] = [p[1]]


# 116是连续施放多个技能效果，因为会调用其他技能，所以定义在外面了
# def skill_type_116(result, skill_id, skill_data):
#     pass

# 综合回复技能
def skill_type_117(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)
    p[1] = get_times(p[1])
    p[3] = get_times(p[3])

    temp_text = []
    # 三种加血方式只写一种
    if p[1] > 0:
        assert (p[2] == 0 and p[3] == 0)
        temp_text.append(f'回复自身回复力{p[1]}倍的HP')
        result['detail']['rec_heal'] = [p[1]]
    elif p[2] > 0:
        assert (p[1] == 0 and p[3] == 0)
        temp_text.append(f'HP回复{p[2]}点')
        result['detail']['fixed_heal'] = [p[2]]
    elif p[3] > 0:
        assert (p[1] == 0 and p[2] == 0)
        if p[3] >= 100:
            temp_text.append(f'HP完全回复')
        else:
            temp_text.append(f'HP回复最大值的{p[3]}%')
        result['detail']['percent_heal'] = [p[3]]

    if p[0] == p[4] != 0:
        if p[0] == 9999:
            temp_text.append(f'绑定状态和觉醒无效状态全回复')
        else:
            temp_text.append(f'绑定状态和觉醒无效状态{p[0]}回合回复')
    else:
        if p[0] == 9999:
            temp_text.append(f'绑定状态全回复')
        elif p[0] > 0:
            temp_text.append(f'绑定状态{p[0]}回合回复')
        if p[4] == 9999:
            temp_text.append(f'觉醒无效状态全回复')
        elif p[4] > 0:
            temp_text.append(f'觉醒无效状态{p[0]}回合回复')
    result['desc_cn'].append('，'.join(temp_text))
    result['detail']['bind_heal'] = [p[0]]
    result['detail']['as_invalid_heal'] = [p[4]]


# 118是随机施放一个技能效果，因为会调用其他技能，所以定义在外面了
# def skill_type_118(result, skill_id, skill_data):
#     pass


# 提升宝珠掉落几率
def skill_type_126(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    up_list = bitmap_to_flag_array(p[0])
    if p[1] == p[2]:
        result['desc_cn'].append(f'{p[1]}回合内，{get_enable_orb_text(up_list)}掉落率提升{p[3]}%')
    else:
        result['desc_cn'].append(f'{p[1]}～{p[2]}回合内，{get_enable_orb_text(up_list)}掉落率提升{p[3]}%')
    result['detail']['orb_rate_up'] = [p[1], p[2], p[3], up_list]


# 列转珠
def skill_type_127(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type']['column'] = True
    result['detail']['column_map'] = [0, 0, 0, 0, 0, 0]
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)

    temp_text = []
    for index in [0, 2]:
        if p[index] == 0:
            continue
        col_change_list = bitmap_to_flag_array(p[index], 6)
        to_list = bitmap_to_flag_array(p[index+1])
        temp_text.append(f'{get_col_text(col_change_list)}变成{get_enable_orb_text(to_list)}')
        result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list)
        result['detail']['column_map'] = union_array(result['detail']['column_map'], col_change_list)
    result['desc_cn'].append('，'.join(temp_text))


# 行转珠
def skill_type_128(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)

    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type']['row'] = True
    result['detail']['row_map'] = [0, 0, 0, 0, 0]
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)

    temp_text = []
    for index in [0, 2]:
        if p[index] == 0:
            continue
        row_change_list = bitmap_to_flag_array(p[index], 5)
        to_list = bitmap_to_flag_array(p[index+1])
        temp_text.append(f'{get_row_text(row_change_list)}变成{get_enable_orb_text(to_list)}')
        result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list)
        result['detail']['row_map'] = union_array(result['detail']['row_map'], row_change_list)
    result['desc_cn'].append('，'.join(temp_text))


# 修改宝珠移动时间
def skill_type_132(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    assert (p[1] * p[2] == 0)  # 两者之间应该有一个是0
    if p[1] != 0:
        p[1] = get_times(p[1], 10)
        if p[1] > 0:
            result['desc_cn'].append(f'{p[0]}回合内，宝珠移动时间增加{p[1]}秒')
        else:
            result['desc_cn'].append(f'{p[0]}回合内，宝珠移动时间减少{p[1]}秒')
    elif p[2] > 0:
        p[2] = get_times(p[2])
        result['desc_cn'].append(f'{p[0]}回合内，宝珠移动时间变为{p[2]}倍')

    result['detail']['move_buff'] = [p[0], p[1], p[2]]


# 强化宝珠（复数属性版）
# TODO：换图标
def skill_type_140(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    power_up_list = bitmap_to_flag_array(p[0])
    result['desc_cn'].append(f'强化{get_enable_orb_text(power_up_list)}（每颗提升伤害{p[1]}%）')
    if 'orb_power' not in result['detail']:
        result['detail']['orb_power'] = get_blank_orb_buff_map()
    for orb_id in range(6):
        result['detail']['orb_power'][orb_id] = power_up_list[orb_id]
    result['detail']['orb_power']['m'] = p[1]


# 生成宝珠（复数属性版）
def skill_type_141(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    to_list = bitmap_to_flag_array(p[1])
    exclude_list = bitmap_to_flag_array(p[2])

    if len(exclude_list) == 0:
        result['desc_cn'].append(f'随机生成{p[0]}颗{get_enable_orb_text(to_list)}')
    else:
        result['desc_cn'].append(f'在{get_enable_orb_text(exclude_list)}之外，随机生成{p[0]}颗{get_enable_orb_text(to_list)}')

    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list)


# 自身属性变化
def skill_type_142(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    result['desc_cn'].append(f'{p[0]}回合内，自身变为{element(p[1])}')
    result['detail']['ele_change'] = [p[0], p[1]]


# 按队伍HP造成属性伤害（目前只有一例，数值可能不对）
def skill_type_143(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    p[0] = get_times(p[0])

    result['desc_cn'].append(f'对敌方{"1" if p[1] == 1 else "全"}体造成队伍HP{p[0]}倍的{element(p[2])}属性伤害')
    if p[2] == 1:
        result['detail']['team_ele_damage_single'] = [99, p[0], p[2]]
    else:
        result['detail']['team_ele_damage_all'] = [99, p[0], p[2]]


# 按队伍攻击力造成属性伤害
def skill_type_144(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[1] = get_times(p[1])

    attack_base = bitmap_to_flag_array(p[0], 5)

    result['desc_cn'].append(f'对敌方{"1" if p[2] == 1 else "全"}体造成队伍{get_ele_atk_text(attack_base)}{p[1]}倍的{element(p[3])}属性伤害')
    if p[2] == 1:
        result['detail']['team_ele_damage_single'] = [sum(attack_base), p[1], p[3]]
    else:
        result['detail']['team_ele_damage_all'] = [sum(attack_base), p[1], p[3]]


# 按队伍回复力回复HP
def skill_type_145(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[0] = get_times(p[0])
    result['desc_cn'].append(f'回复队伍回复力{p[0]}倍的HP')
    result['detail']['team_rec_heal'] = [p[0]]


# 其他角色技能加速
def skill_type_146(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    if p[0] == p[1]:
        result['desc_cn'].append(f'自身以外其他我方技能冷却时间缩短{p[0]}回合')
    else:
        result['desc_cn'].append(f'自身以外其他我方技能冷却时间缩短{p[0]}～{p[1]}回合')

    result['detail']['skill_boost'] = [p[0], p[1]]
