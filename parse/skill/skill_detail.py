from .type_parse import *

temp = []


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

        try:
            eval(f'skill_type_{skill_data[skill_id].skill_type}(result, skill_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

    z = 1
    return result


def get_leader_skill_detail(skill_id, skill_data):
    return {}


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

        try:
            eval(f'skill_type_{sub_skill_info.skill_type}(result, sub_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

    skill_desc_count_map = {}
    for skill_desc in result['desc_cn']:
        if skill_desc not in skill_desc_count_map:
            skill_desc_count_map[skill_desc] = 1
        else:
            skill_desc_count_map[skill_desc] += 1

    result['desc_cn'].clear()
    for desc, desc_count in skill_desc_count_map.items():
        result['desc_cn'].append(f'{desc}{f"×{desc_count}次" if desc_count > 1 else ""}')

