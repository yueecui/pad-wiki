from .skill_common import *


# 全体攻击buff
def skill_type_51(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，所有攻击变为全体攻击')
    result['detail']['all_attack'] = [p[0]]


# 强化宝珠
# TODO：换图标
def skill_type_52(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'强化{orb(p[0])}（每颗提升伤害{p[1]}%）')
    if 'orb_power' not in result['detail']:
        result['detail']['orb_power'] = get_blank_orb_buff_map()
    result['detail']['orb_power'][p[0]] = 1
    result['detail']['orb_power']['m'] = p[1]


# 对敌方1体造成固定伤害
# 与188的区别应该是188都是多次连续伤害，55是单次的
def skill_type_55(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'对敌方1体造成{p[0]}点无视防御的固定伤害')
    result['detail']['flat_damage_single'] = [p[0], 1]


# 对敌方全体造成固定伤害
def skill_type_56(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'对敌方全体造成{p[0]}点无视防御的固定伤害')
    result['detail']['flat_damage_all'] = [p[0]]


# 随机倍率指定属性全体攻击技能
def skill_type_58(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])
    p[2] = get_times(p[2])
    if p[1] == p[2]:
        result['desc_cn'].append(f'对敌方全体造成自身攻击力{p[1]}倍的{element(p[0])}伤害')
    else:
        result['desc_cn'].append(f'对敌方全体造成自身攻击力随机{p[1]}～{p[2]}倍的{element(p[0])}伤害')
    result['detail']['ele_damage_all'] = [p[0], p[2], p[1]]


# 随机倍率指定属性单体攻击技能
def skill_type_59(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])
    p[2] = get_times(p[2])
    if p[1] == p[2]:
        result['desc_cn'].append(f'对敌方1体造成自身攻击力{p[1]}倍的{element(p[0])}伤害')
    else:
        result['desc_cn'].append(f'对敌方1体造成自身攻击力随机{p[1]}～{p[2]}倍的{element(p[0])}伤害')
    result['detail']['ele_damage_single'] = [p[0], p[2], p[1]]


# 反击buff
def skill_type_60(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'{p[0]}回合内，受到伤害时进行反击，对敌方全体造成自身攻击力{p[1]}倍的{element(p[2])}伤害')
    result['detail']['counter_attack'] = [p[0], p[1], p[2]]


# 洗版
def skill_type_71(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    to_list = list_to_orb_array(p)
    result['desc_cn'].append(f'全部宝珠变成{get_enable_orb_text(to_list)}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_from'] = bitmap_to_flag_array(1023)
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list)
    result['detail']['all'] = True


# 自残+对敌1体指定属性攻击
def skill_type_84(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[1] = get_times(p[1])
    p[2] = get_times(p[2])

    if p[3] == 0:
        before_text = 'HP变为1，'
    else:
        before_text = f'HP变为当前的{p[3]}%，'

    if p[1] == p[2]:
        result['desc_cn'].append(f'{before_text}对敌方1体造成自身攻击力{p[2]}倍的{element(p[0])}伤害')
    else:
        result['desc_cn'].append(f'{before_text}对敌方1体造成自身攻击力{p[1]}～{p[2]}倍的{element(p[0])}伤害')
    result['detail']['ele_damage_single'] = [p[0], p[2], p[1]]
    result['detail']['consume_hp'] = [p[3]]


# 自残+对敌全体指定属性攻击
def skill_type_85(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[1] = get_times(p[1])
    p[2] = get_times(p[2])

    if p[3] == 0:
        before_text = 'HP变为1，'
    else:
        before_text = f'HP变为当前的{p[3]}%，'

    if p[1] == p[2]:
        result['desc_cn'].append(f'{before_text}对敌方全体造成自身攻击力{p[2]}倍的{element(p[0])}伤害')
    else:
        result['desc_cn'].append(f'{before_text}对敌方全体造成自身攻击力{p[1]}～{p[2]}倍的{element(p[0])}伤害')
    result['detail']['ele_damage_all'] = [p[0], p[2], p[1]]
    result['detail']['consume_hp'] = [p[3]]


# 自残+对敌1体指定属性固定伤害
def skill_type_86(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[1] = get_times(p[1])
    p[2] = get_times(p[2])

    if p[3] == 0:
        before_text = 'HP变为1，'
    else:
        before_text = f'HP变为当前的{p[3]}%，'

    result['desc_cn'].append(f'{before_text}对敌方1体造成固定{p[1]}点{element(p[0])}伤害')
    result['detail']['fixed_ele_damage_single'] = [p[0], p[1]]
    result['detail']['consume_hp'] = [p[3]]


# 单类型攻击力buff
def skill_type_88(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    p[2] = get_times(p[2])
    result['desc_cn'].append(f'{p[0]}回合内，{monster_type(p[1])}宠物攻击力变为{p[2]}倍')
    if 'atk_buff' not in result['detail']:
        result['detail']['atk_buff'] = get_blank_atk_buff_map()
    result['detail']['atk_buff']['t'] = p[0]
    result['detail']['atk_buff']['m'] = p[2]
    result['detail']['atk_buff'][p[1] + 10] = 1


# 双属性攻击力buff（也包括回复力）
# TODO：转为珠子图标
def skill_type_90(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[3] = get_times(p[3])
    result['desc_cn'].append(f'{p[0]}回合内，{element_buff(p[1])}和{element_buff(p[2])}变为{p[3]}倍')
    if 'atk_buff' not in result['detail']:
        result['detail']['atk_buff'] = get_blank_atk_buff_map()
    result['detail']['atk_buff']['t'] = p[0]
    result['detail']['atk_buff']['m'] = p[3]
    result['detail']['atk_buff'][p[1]] = 1
    result['detail']['atk_buff'][p[2]] = 1


# 双强化宝珠
# TODO：换图标
def skill_type_91(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'强化{orb(p[0])}和{orb(p[1])}（每颗提升伤害{p[2]}%）')
    if 'orb_power' not in result['detail']:
        result['detail']['orb_power'] = get_blank_orb_buff_map()
    result['detail']['orb_power'][p[0]] = 1
    result['detail']['orb_power'][p[1]] = 1
    result['detail']['orb_power']['m'] = p[2]


# 双类型攻击力buff
def skill_type_92(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 4)
    p[3] = get_times(p[3])
    result['desc_cn'].append(f'{p[0]}回合内，{monster_type(p[1])}和{monster_type(p[2])}宠物攻击力变为{p[3]}倍')
    if 'atk_buff' not in result['detail']:
        result['detail']['atk_buff'] = get_blank_atk_buff_map()
    result['detail']['atk_buff']['t'] = p[0]
    result['detail']['atk_buff']['m'] = p[3]
    result['detail']['atk_buff'][p[1] + 10] = 1
    result['detail']['atk_buff'][p[2] + 10] = 1


# 更换队长
def skill_type_93(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'将自己换成队长，再次使用此技能则换回原来的队长')
    result['detail']['sub_leader'] = True
