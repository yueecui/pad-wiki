from .skill_common import *


# 宝珠锁定
def skill_type_152(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    lock_list = bitmap_to_flag_array(p[0])
    result['desc_cn'].append(f'锁定{get_enable_orb_text(lock_list)}')
    result['detail']['orb_lock'] = lock_list


# 敌人属性转换
def skill_type_153(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'将敌方全体变为{element(p[0])}')
    result['detail']['enemy_ele_change'] = [p[0]]


# 多重转珠（表对表）
def skill_type_154(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    from_list = bitmap_to_flag_array(p[0])
    to_list = bitmap_to_flag_array(p[1])
    result['desc_cn'].append(f'{get_enable_orb_text(from_list)}变成{get_enable_orb_text(to_list)}')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    if 'turn_from' not in result['detail']:
        result['detail']['turn_from'] = bitmap_to_flag_array(0)
    result['detail']['turn_from'] = union_array(result['detail']['turn_from'], from_list)
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'] = union_array(result['detail']['turn_to'], to_list)
    if sum(result['detail']['turn_from']) == len(result['detail']['turn_from']):
        result['detail']['all'] = True


# 根据队伍特定觉醒数量产生效果
def skill_type_156(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    if p[4] == 1:  # 根据觉醒回血
        aw_sk_info = get_awakening_skill_info(p[1:4])
        result['desc_cn'].append(f'根据队伍中{aw_sk_info[0]}的觉醒数回复HP，每个觉醒回复{p[5]}点HP')
        result['detail']['awakening_heal'] = [p[5], p[1], p[2], p[3]]
    elif p[4] == 2:  # 根据觉醒提升攻击力
        p[5] -= 100
        aw_sk_info = get_awakening_skill_info(p[1:4])
        result['desc_cn'].append(f'{p[0]}回合内，根据队伍中{aw_sk_info[0]}的觉醒数提升攻击力，每个觉醒提升{p[5]}%')
        result['detail']['awakening_atk'] = [p[0], p[5], p[1], p[2], p[3]]
    elif p[4] == 3:  # 根据觉醒减少受到的伤害
        aw_sk_info = get_awakening_skill_info(p[1:4])
        result['desc_cn'].append(f'{p[0]}回合内，根据队伍中{aw_sk_info[0]}的觉醒数减少受到伤害，每个觉醒减少{p[5]}%')
        result['detail']['awakening_cut'] = [p[0], p[5], p[1], p[2], p[3]]


# 一段时间内增加combo
def skill_type_160(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，结算时增加{p[1]} COMBO{"S" if p[1]>1 else ""}')
    result['detail']['combo_buff'] = [p[0], p[1]]


# 重力（最大百分比）
def skill_type_161(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'敌方全体损失最大HP的{p[0]}%')
    result['detail']['max_percent_damage'] = [p[0]]


# 根据队伍特定觉醒数量提升攻击力
# 与156相比，只能写攻击力，目前的例子都是和156同时使用，可能是什么特殊的判定导致不能写2个156
def skill_type_168(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 8)
    aw_sk_info = get_awakening_skill_info(p[1:4])
    result['desc_cn'].append(f'{p[0]}回合内，根据队伍中{aw_sk_info[0]}的觉醒数提升攻击力，每个觉醒提升{p[7]}%')
    result['detail']['awakening_atk'] = [p[0], p[7], p[1], p[2], p[3]]


# 宝珠解锁
def skill_type_172(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'所有宝珠解锁锁定')
    result['detail']['unlock_all'] = [True]


# 敌方buff无效
def skill_type_173(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
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


# 形状转珠
def skill_type_176(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    shape_info = get_shape_info(p[0:5])

    result['desc_cn'].append(f'{shape_info[0]}生成{orb(p[5])}宝珠')
    if 'turn_type' not in result['detail']:
        result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type']['shape'] = True
    result['detail']['shape_map'] = p[0:5]
    result['detail']['shape_type'] = shape_info[1]
    if 'turn_to' not in result['detail']:
        result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'][p[5]] = 1


# 持续回复技能，外加绑定和觉醒无效解除
def skill_type_179(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 5)

    temp_text = []
    if p[1] > 0:
        assert p[2] == 0
        temp_text.append(f'{p[0]}回合内，每回合回复{p[1]}点HP')
        result['detail']['fixed_hot'] = [p[0], p[1]]
    elif p[2] > 0:
        assert p[1] == 0
        if p[2] >= 100:
            temp_text.append(f'{p[0]}回合内，每回合HP完全回复')
        else:
            temp_text.append(f'{p[0]}回合内，每回合HP回复最大值的{p[2]}%')
        result['detail']['percent_hot'] = [p[0], p[2]]

    if p[3] == p[4] != 0:
        if p[3] == 9999:
            temp_text.append(f'绑定状态和觉醒无效状态全回复')
        else:
            temp_text.append(f'绑定状态和觉醒无效状态{p[0]}回合回复')
    else:
        if p[3] == 9999:
            temp_text.append(f'绑定状态全回复')
        elif p[3] > 0:
            temp_text.append(f'绑定状态{p[0]}回合回复')
        if p[4] == 9999:
            temp_text.append(f'觉醒无效状态全回复')
        elif p[4] > 0:
            temp_text.append(f'觉醒无效状态{p[0]}回合回复')

    result['desc_cn'].append('，'.join(temp_text))
    result['detail']['bind_heal'] = [p[3]]
    result['detail']['as_invalid_heal'] = [p[4]]


# 强化宝珠掉落率提升
def skill_type_180(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，强化宝珠掉落率提升{p[1]}%')
    result['detail']['power_orb_drop_rate'] = [p[0], p[1]]


# 掉落宝珠不计算combo
def skill_type_184(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，掉落宝珠不产生Combo')
    result['detail']['no_drop_combo'] = [p[0]]


# 对敌方1体造成固定伤害
# 与55基本一样，只是用于连续造成多次伤害（配置ID不同可能和动画速度有关）
def skill_type_188(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'对敌方1体造成{p[0]}点无视防御的固定伤害')
    if 'f_damage_single' in result['detail']:
        result['detail']['flat_damage_single'][0] += p[0]
        result['detail']['flat_damage_single'][1] += 1  # 记录总攻击次数
    else:
        result['detail']['flat_damage_single'] = [p[0], 1]


# 特殊专用技能
def skill_type_189(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'所有宝珠解锁锁定')
    result['detail']['unlock_all'] = [True]

    result['detail']['turn_type'] = get_blank_turn_type_map()
    result['detail']['turn_type']['all'] = True
    result['detail']['turn_to'] = bitmap_to_flag_array(0)
    result['detail']['turn_to'][0] = 1
    result['detail']['turn_to'][1] = 1
    result['detail']['turn_to'][2] = 1
    result['detail']['turn_to'][3] = 1
    result['desc_cn'].append(f'所有宝珠变成{get_enable_orb_text(result["detail"]["turn_to"])}')

    result['desc_cn'].append(f'显示3 Combos的转珠路线（普通地下城＆三消模式限定）')


# 伤害无效贯通
def skill_type_191(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    result['desc_cn'].append(f'{p[0]}回合内，攻击可以贯通伤害无效状态')
    result['detail']['damage_immunity_invalid'] = [p[0]]


# 自残
def skill_type_195(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 1)
    if p[0] == 0:
        result['desc_cn'].append('HP变为1')
    else:
        result['desc_cn'].append(f'HP变为当前的{p[0]}%')
    result['detail']['consume_hp'] = [p[0]]


# 无法消除宝珠状态回复
def skill_type_196(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    if p[0] == 9999:
        result['desc_cn'].append(f'无法消除宝珠状态完全回复')
    else:
        result['desc_cn'].append(f'无法消除宝珠状态{p[0]}回合回复')
    result['detail']['drop_ban_heal'] = [p[0]]
