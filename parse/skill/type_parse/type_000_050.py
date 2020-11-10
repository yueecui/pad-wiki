from .skill_common import *


# 倍率属性全体攻击技能
def skill_type_0(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'对敌方全体造成自身攻击力{p[1]}倍的{element(p[0])}伤害')
    result['detail']['ele_damage_all'] = [p[0], p[1], 0]


# 固定数值属性全体攻击技能
def skill_type_1(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'对敌方全体造成固定{p[1]}点{element(p[0])}伤害')
    result['detail']['fixed_ele_damage_all'] = [p[0], p[1]]


# 倍率自属性单体攻击技能
def skill_type_2(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[0] = get_times(p[0])
    result['desc_cn'].append(f'对敌方1体造成自身攻击力{p[0]}倍的自身主属性伤害')
    result['detail']['self_ele_damage_single'] = [10, p[0], 0]


# 受到伤害减少
def skill_type_3(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    if p[1] >= 100:
        result['desc_cn'].append(f'{p[0]}回合内，受到的伤害无效化')
    else:
        result['desc_cn'].append(f'{p[0]}回合内，受到的所有伤害减少{p[1]}%')
    result['detail']['damage_cut'] = [p[0], p[1]]


# 中毒
def skill_type_4(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[0] = get_times(p[0])
    result['desc_cn'].append(f'对敌方全体中毒，每回合损失宠物自身攻击力{p[0]}倍的HP')
    result['detail']['poison'] = [p[0]]


# 时间停止
def skill_type_5(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'{p[0]}秒内，时间停止，可以自由移动宝珠')
    result['detail']['the_world'] = [p[0]]


# 重力
def skill_type_6(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'敌方全体损失当前HP {p[0]}%的HP')
    result['detail']['percent_damage'] = [p[0]]


# 固定数值回复HP
def skill_type_8(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'HP回复{p[0]}点')
    result['detail']['fixed_heal'] = [p[0]]


# 转珠，一转一
def skill_type_9(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 2)
    result['desc_cn'].append(f'{orb(p[0])}变成{orb(p[1])}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    assert result['detail']['turn_type']['count'] == 0
    result['detail']['turn_type']['count'] = 1
    if 'turn_from' not in result['detail']:
        result['detail']['turn_from'] = flag_to_orb_array(0)
    result['detail']['turn_from'][p[0]] = True
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = flag_to_orb_array(0)
    result['detail']['turn_to'][p[1]] = True


# 全画面宝珠刷新
def skill_type_10(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'全画面宝珠刷新')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type']['refresh'] = True


# 威吓
def skill_type_18(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'敌方的行动间隔延长{p[0]}回合')
    result['detail']['slow'] = [p[0]]


# 破防
def skill_type_19(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'{p[0]}回合内，敌方的防御力减少{p[1]}%')
    result['detail']['break_armor'] = [p[0], p[1]]


# 转珠，二转二
def skill_type_20(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 4)
    if p[1] == p[3]:
        result['desc_cn'].append(f'{orb(p[0])}和{orb(p[2])}变成{orb(p[1])}')
    else:
        result['desc_cn'].append(f'{orb(p[0])}变成{orb(p[1])}，{orb(p[2])}变成{orb(p[3])}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    assert result['detail']['turn_type']['count'] == 0
    result['detail']['turn_type']['count'] = 2
    if 'turn_from' not in result['detail']:
        result['detail']['turn_from'] = flag_to_orb_array(0)
    result['detail']['turn_from'][p[0]] = True
    result['detail']['turn_from'][p[2]] = True
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = flag_to_orb_array(0)
    result['detail']['turn_to'][p[1]] = True
    result['detail']['turn_to'][p[3]] = True


# 倍率自属性单体攻击技能
def skill_type_35(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[0] = get_times(p[0])
    result['desc_cn'].append(f'对敌方1体造成自身攻击力{p[0]}倍的自身主属性伤害，并回复伤害{p[1]}%的HP')
    result['detail']['self_ele_damage_single'] = [10, p[0], 0]
    result['detail']['absorb_heal'] = [p[1]]


# 对特定敌方属性造成属性伤害
def skill_type_42(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'对所有{element(p[0])}敌方造成固定{p[2]}点{element(p[1])}伤害')
    result['detail']['ele_damage_by_ele'] = [p[1], p[2], p[0]]


# 属性攻击力buff（也包括回复力）
def skill_type_50(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 3)
    p[2] = get_times(p[2])
    if 0 <= p[1] <= 4:
        result['desc_cn'].append(f'{p[0]}回合内，{ORB_MAP[p[1]]}属性攻击力变为{p[2]}倍')
        if 'atk_buff' not in result['detail']:
            result['detail']['atk_buff'] = get_blank_atk_buff_map()
        result['detail']['atk_buff']['t'] = p[0]
        result['detail']['atk_buff'][p[1]] = p[2]
    elif p[1] == 5:
        result['desc_cn'].append(f'{p[0]}回合内，回复力变为{p[2]}倍')
        result['detail']['rec_buff'] = [p[0], p[2]]
    else:
        raise Exception(f'预料外的宝珠类型：{p[1]}')
