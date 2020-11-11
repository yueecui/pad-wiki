from .skill_common import *


# 按属性、类型
def skill_type_185(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    p[0] = get_times(p[0])  # 移动时间
    p[3] = get_times(p[3])  # HP
    p[4] = get_times(p[4])  # 攻击力
    p[5] = get_times(p[5])  # 回复力

    leader_buff = get_blank_leader_buff(p[1], p[2])
    leader_buff['hp'] = p[3] if p[3] > 0 else 1
    leader_buff['atk'] = p[4] if p[4] > 0 else 1
    leader_buff['rec'] = p[5] if p[5] > 0 else 1
    leader_buff['time'] = p[0]

    temp_text = []
    if p[3] == p[4] == p[5] > 0:
        temp_text.append(f'全属性变为{p[3]}倍')
    elif p[3] == p[5] > 0:
        temp_text.append(f'HP和回复力变为{p[3]}倍')
        if p[4] > 0:
            temp_text.append(f'攻击力变为{p[4]}倍')
    else:
        if p[3] > 0:
            temp_text.append(f'HP变为{p[3]}倍')
        if p[4] > 0:
            temp_text.append(f'攻击力变为{p[4]}倍')
        if p[5] > 0:
            temp_text.append(f'回复力变为{p[5]}倍')

    result['desc_cn'].append(f'{get_pet_category_text(leader_buff)}的宠物{"、".join(temp_text)}'
                             f'{f"。宝珠操作时间延长{p[0]}秒" if p[0] > 0 else ""}')
    if 'leader_buff' not in result['detail']:
        result['detail']['leader_buff'] = get_blank_leader_buff(0, 0)
    union_leader_buff(result['detail']['leader_buff'], leader_buff)
