from .skill_common import *


# 按属性、类型被动强化三围和移动时间
def skill_type_185(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)
    time_m = get_times(p[0])  # 移动时间
    hp_m = get_times(p[3])  # HP
    atk_m = get_times(p[4])  # 攻击力
    rec_m = get_times(p[5])  # 回复力

    pet_category = convert_pet_category(p[1], p[2])

    result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}'
                             f'{f"。宝珠操作时间延长{time_m}秒" if time_m > 0 else ""}')

    leader_buff = get_blank_leader_buff()
    leader_buff['hp'] = hp_m if hp_m > 0 else 1
    leader_buff['atk'] = atk_m if atk_m > 0 else 1
    leader_buff['rec'] = rec_m if rec_m > 0 else 1
    leader_buff['time'] = time_m
    update_leader_buff(result, leader_buff, pet_category)
