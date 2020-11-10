from .skill_common import *


# 多重转珠（表对表）
def skill_type_154(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    from_list = flag_to_orb_array(p[0])
    to_list = flag_to_orb_array(p[1])
    result['desc_cn'].append(f'{get_enable_orb_text(from_list)}变成{get_enable_orb_text(to_list)}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    if 'turn_from' not in result['detail']:
        result['detail']['turn_from'] = flag_to_orb_array(0)
    result['detail']['turn_from'] = union_orb_array(result['detail']['turn_from'], from_list)
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = flag_to_orb_array(0)
    result['detail']['turn_to'] = union_orb_array(result['detail']['turn_to'], to_list)
    result['detail']['turn_type']['count'] = sum(result['detail']['turn_from'])
    if result['detail']['turn_type']['count'] == len(result['detail']['turn_from']):
        result['detail']['all'] = True


# 一段时间内增加combo
def skill_type_160(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'{p[0]}回合内，结算时增加{p[1]} COMBO{"S" if p[1]>1 else ""}')
    result['detail']['combo_buff'] = [p[0], p[1]]


# 敌方buff无效
def skill_type_173(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 4)
    type_list = []
    if p[1] == 1:
        type_list.append('属性吸收')
        result['detail']['ele_absorb_invalid'] = [p[0]]
    if p[3] == 1:
        type_list.append('伤害吸收')
        result['detail']['damage_absorb_invalid'] = [p[0]]
    assert len(type_list) > 0
    result['desc_cn'].append(f'{p[0]}回合内，{"和".join(type_list)}无效化')


# 对敌方1体造成固定伤害
# 与55基本一样，只是用于连续造成多次伤害（配置ID不同可能和动画速度有关）
def skill_type_188(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'对敌方1体造成{p[0]}点无视防御的固定伤害')
    if 'f_damage_single' in result['detail']:
        result['detail']['flat_damage_single'][0] += p[0]
        result['detail']['flat_damage_single'][1] += 1  # 记录总攻击次数
    else:
        result['detail']['flat_damage_single'] = [p[0], 1]
