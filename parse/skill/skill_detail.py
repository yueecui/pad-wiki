from .type_parse import *

temp = []


def get_active_skill_detail(skill_id, skill_data):
    result = {
        'id': skill_id,
        'name': skill_data[skill_id].name,
        'desc_jp': skill_data[skill_id].description,
        'desc_cn': [],
        'max_level': skill_data[skill_id].levels,
        'turn_max': skill_data[skill_id].turn_max,
        'turn_min': skill_data[skill_id].turn_min,
        'type': skill_data[skill_id].skill_type,
        'params': skill_data[skill_id].params,
        'detail': {}
    }

    if skill_id > 0:
        try:
            eval(f'skill_type_{skill_data[skill_id].skill_type}(result, skill_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

    return result


def get_leader_skill_detail(skill_id, skill_data):
    result = {
        'id': skill_id,
        'name': skill_data[skill_id].name,
        'desc_jp': skill_data[skill_id].description,
        'desc_cn': [],
        'type': skill_data[skill_id].skill_type,
        'params': skill_data[skill_id].params,
        'detail': {}
    }

    # 特殊卡的处理
    # 蛋龙
    if skill_data[skill_id].skill_type == 48:
        if result['id'] in [859]:
            result['desc_cn'] = '作为合成素材时，将会解放宠物的觉醒技能'
        elif result['id'] in [860, 1600, 2486]:
            result['desc_cn'] = '作为合成素材时，将有几率解放宠物的觉醒技能'
    elif skill_data[skill_id].skill_type == 121:
        if result['id'] in [1911, 1912, 1913, 1914, 1915]:
            result['desc_cn'] = f'作为{element(result["id"] - 1911)}属性宠物的合成素材时，将必定提升宠物1级技能'

    # 正常处理
    elif skill_id > 0:
        try:
            eval(f'skill_type_{skill_data[skill_id].skill_type}(result, skill_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

    return result


# 主动技能：连续施放多个技能效果
def skill_type_116(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

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


# 主动技能：随机施放一个技能效果
def skill_type_118(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    result['desc_cn'].append(f'随机发动以下{len(p)}个技能之一')
    result['random_skill'] = []
    result['detail']['random_effect'] = [True]
    # 错误检查
    # 判断会重复同一个子技能多次的都是单体固定伤害
    for random_sk_id in p:
        random_sk_info = {
            'name': skill_data[random_sk_id].name,
            'desc_cn': [],
            'detail': {}
        }
        try:
            eval(f'skill_type_{skill_data[random_sk_id].skill_type}(random_sk_info, random_sk_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

        del random_sk_info['detail']
        result['random_skill'].append(random_sk_info)


# 队长技能：合并多个技能效果
def skill_type_138(result, skill_id, skill_data):
    p = list(skill_data[skill_id].params)

    for sub_id in p:
        sub_skill_info = skill_data[sub_id]

        try:
            eval(f'skill_type_{sub_skill_info.skill_type}(result, sub_id, skill_data)')
        except NameError as e:
            error = str(e)
            if error not in temp:
                temp.append(error)
                print(error)

