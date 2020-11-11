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


# 封印自己技能
def skill_type_214(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，无法使用技能')
    result['detail']['skill_seal'] = [p[0]]

