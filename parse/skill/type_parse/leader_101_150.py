from .skill_common import *


# 按属性、类型被动强化三围和受到属性伤害减少
def skill_type_129(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)
    add_zero(p, 6)

    leader_buff = get_blank_leader_buff()
    pet_category = convert_pet_category(p[0], p[1])

    if p[0] + p[1] > 0:
        hp_m = get_times(p[2])  # HP
        atk_m = get_times(p[3])  # 攻击力
        rec_m = get_times(p[4])  # 回复力

        result['desc_cn'].append(f'{get_pet_category_text(pet_category)}宠物的{get_pet_status_text(hp_m, atk_m, rec_m)}')

        leader_buff['hp'] = hp_m if hp_m > 0 else 1
        leader_buff['atk'] = atk_m if atk_m > 0 else 1
        leader_buff['rec'] = rec_m if rec_m > 0 else 1

    if p[5] > 0:
        enemy_category = convert_pet_category(p[5])
        result['desc_cn'].append(f'被{get_pet_category_text(enemy_category)}敌人攻击时，受到的伤害减少{p[6]}%')

        leader_buff['ele_d_rate'] = [100, 100, 100, 100, 100]
        for ele_id in range(0, 5):
            if enemy_category[ele_id]:
                leader_buff['ele_d_rate'][ele_id] = 100 - p[6]

    update_leader_buff(result, leader_buff, pet_category)
