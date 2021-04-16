from .skill_common import *


# 变身
def skill_type_202(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'变身为<Pet:{p[0]}>')
    result['detail']['transform'] = [p[0]]


# 掉落锁定珠
def skill_type_205(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    if p[0] == -1:
        p[0] = 1023
    lock_list = bitmap_to_flag_array(p[0])
    result['desc_cn'].append(f'{p[1]}回合内，{get_enable_orb_text(lock_list)}以锁定状态掉落')
    result['detail']['orb_lock_drop'] = [p[1], lock_list]


# 宝珠轮盘
def skill_type_207(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    p[1] = get_times(p[1])
    result['desc_cn'].append(f'{p[0]}回合内，随机{p[7]}个位置上的宝珠每隔{p[1]}秒不断转换')
    result['detail']['orb_roulette'] = [p[0], p[1], p[7]]


# 生成两种宝珠
def skill_type_208(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 3)
    to_list_a = bitmap_to_flag_array(p[0])
    to_number_a = p[1]
    to_list_b = bitmap_to_flag_array(p[4])
    to_number_b = p[3]
    exclude_list = bitmap_to_flag_array(p[2])

    if len(exclude_list) == 0:
        result['desc_cn'].append(f'随机生成{to_number_a}颗{get_enable_orb_text(to_list_a)}和'
                                 f'{to_number_b}颗{get_enable_orb_text(to_list_b)}')
    else:
        result['desc_cn'].append(f'在{get_enable_orb_text(exclude_list)}之外，'
                                 f'随机生成{to_number_a}颗{get_enable_orb_text(to_list_a)}和'
                                 f'{to_number_b}颗{get_enable_orb_text(to_list_b)}')

    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type'][4] = 1
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list_a)
    result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list_b)


# 其他角色技能减速
def skill_type_218(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 2)
    if p[0] == p[1]:
        result['desc_cn'].append(f'自身以外其他我方技能冷却时间延长{p[0]}回合')
    else:
        result['desc_cn'].append(f'自身以外其他我方技能冷却时间延长{p[0]}～{p[1]}回合')

    result['detail']['skill_slow'] = [p[0], p[1]]


# 封印自己技能
def skill_type_214(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，无法使用技能')
    result['detail']['skill_seal'] = [p[0]]

