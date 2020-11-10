from .skill_common import *


# 生成宝珠
# TODO：换图标
def skill_type_52(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'强化{orb(p[0])}')
    if 'orb_power' not in result['detail']:
        result['detail']['orb_power'] = flag_to_orb_array(0)
    result['detail']['orb_power'][p[0]] = True


# 对敌方1体造成固定伤害
# 与188的区别应该是188都是多次连续伤害，55是单次的
def skill_type_55(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'对敌方1体造成{p[0]}点无视防御的固定伤害')
    result['detail']['flat_damage_single'] = [p[0], 1]


# 洗版
def skill_type_71(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    to_list = list_to_orb_array(p)
    result['desc_cn'].append(f'全部宝珠变成{get_enable_orb_text(to_list)}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_from'] = flag_to_orb_array(1023)
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = flag_to_orb_array(0)
    result['detail']['turn_to'] = union_orb_array(result['detail']['turn_to'], to_list)
    result['detail']['turn_type']['count'] = sum(result['detail']['turn_from'])
    result['detail']['all'] = True


# 单类型攻击力buff
def skill_type_88(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 3)
    p[2] = get_times(p[2])
    result['desc_cn'].append(f'{p[0]}回合内，{monster_type(p[1])}宠物攻击力变为{p[2]}倍')
    if 'atk_buff' not in result['detail']:
        result['detail']['atk_buff'] = get_blank_atk_buff_map()
    result['detail']['atk_buff']['t'] = p[0]
    result['detail']['atk_buff'][p[1] + 10] = p[2]


# 双类型攻击力buff
def skill_type_92(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    add_zero(p, 4)
    p[3] = get_times(p[3])
    result['desc_cn'].append(f'{p[0]}回合内，{monster_type(p[1])}和{monster_type(p[2])}宠物攻击力变为{p[3]}倍')
    if 'atk_buff' not in result['detail']:
        result['detail']['atk_buff'] = get_blank_atk_buff_map()
    result['detail']['atk_buff']['t'] = p[0]
    result['detail']['atk_buff'][p[1] + 10] = p[3]
    result['detail']['atk_buff'][p[2] + 10] = p[3]


# 更换队长
def skill_type_93(result, skill_id, skill_data):
    p = skill_data[skill_id].params
    result['desc_cn'].append(f'将自己换成队长，再次是呀此技能则换回原来的队长')
    result['detail']['sub_leader'] = True
