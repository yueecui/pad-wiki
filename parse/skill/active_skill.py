from .common import *


def get_active_skill_detail(skill_id, skill_data):
    result = {
        'id': skill_id,
        'name': skill_data[skill_id].name,
        'desc_jp': skill_data[skill_id].description,
        'desc_cn': [],
        # 'type': skill_data[skill_id].skill_type,
        'max_level': skill_data[skill_id].levels,
        'turn_max': skill_data[skill_id].turn_max,
        'turn_min': skill_data[skill_id].turn_min,
        # 'params': skill_data[skill_id].params,
        'detail': {}
    }

    if skill_id > 0:
        assert result['max_level'] > 0
        assert result['turn_max'] > 0
        eval(f'skill_type_{skill_data[skill_id].skill_type}(result, skill_id, skill_data)')

    z = 1
    return result


# 除以100获得倍率（int或是float）
def get_times(number):
    number = number/100
    if int(number) == number:
        number = int(number)
    return number


# 获得一个基础的宝珠转换类型表
def get_blank_turn_type_map():
    return {
        0: False,  # 横行
        1: False,  # 竖列
        2: False,  # 洗版
        3: False,  # 15:15洗版
    }


# 获得一个基础的宝珠转换表
def get_blank_turn_map():
    return {
        0: False,  # 火
        1: False,  # 水
        2: False,  # 木
        3: False,  # 光
        4: False,  # 暗
        5: False,  # 回复
        6: False,  # 废
        7: False,  # 毒
        # 8: False,
    }


# 倍率属性全体攻击技能
def skill_type_0(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'对敌方全体造成{p[1]}倍攻击力的{element(p[0])}伤害')
    result['detail']['ele_damage_all'] = [p[0], p[1]]


# 固定数值属性全体攻击技能
def skill_type_1(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'对敌方全体造成固定{p[1]}点{element(p[0])}伤害')
    result['detail']['fixed_ele_damage_all'] = [p[0], p[1]]


# 转珠，一转一
def skill_type_9(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    if len(p) < 2:
        p.append(0)
    result['desc_cn'].append(f'{drop(p[0])}变为{drop(p[1])}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    if 'turn_from' not in result['detail']:
        result['detail']['turn_from'] = get_blank_turn_map()
    result['detail']['turn_from'][p[0]] = True
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = get_blank_turn_map()
    result['detail']['turn_to'][p[1]] = True


# BUFF珠子性能（单buff）
def skill_type_50(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    p[2] = get_times(p[2])
    result['desc_cn'].append(f'{p[0]}回合内，{drop_buff(p[1])}变为{p[2]}倍')
    result['detail'][f'drop_buff_{p[1]}'] = [p[0], p[2]]


# 连续施放多个技能效果
def skill_type_116(result, skill_id, skill_data):
    p = skill_data[skill_id].params

    # 错误检查
    # 判断会重复同一个子技能多次的都是单体固定伤害
    checked_id_list = []
    for sub_id in p:
        if sub_id in checked_id_list:
            assert skill_data[sub_id].skill_type in [188]
        else:
            checked_id_list.append(sub_id)

    for sub_id in p:
        sub_skill_info = skill_data[sub_id]
        eval(f'skill_type_{sub_skill_info.skill_type}(result, sub_id, skill_data)')

    skill_desc_count_map = {}
    for skill_desc in result['desc_cn']:
        if skill_desc not in skill_desc_count_map:
            skill_desc_count_map[skill_desc] = 1
        else:
            skill_desc_count_map[skill_desc] += 1

    result['desc_cn'].clear()
    for desc, desc_count in skill_desc_count_map.items():
        result['desc_cn'].append(f'{desc}{f"×{desc_count}次" if desc_count > 1 else ""}')


# 一段时间内增加combo
def skill_type_160(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'{p[0]}回合内，结算时增加{p[1]} COMBO{"S" if p[1]>1 else ""}')
    result['detail']['extra_combos'] = [p[0], p[1]]


# 对敌方1体造成固定伤害
def skill_type_188(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'对敌方1体造成{p[0]}点无视防御的固定伤害')
    if 'f_damage_single' in result['detail']:
        result['detail']['flat_damage_single'][0] += p[0]
        result['detail']['flat_damage_single'][1] += 1  # 记录总攻击次数
    else:
        result['detail']['flat_damage_single'] = [p[0], 1]
