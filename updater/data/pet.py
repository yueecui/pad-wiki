# 整理card数据
from typing import Dict, Any
from common.pad_types import CardId, PetInfo, EvoType
from parse.raw.skill import load_skill_data
from parse.raw.card import load_card_data
from parse.skill import *


def clean_pet_info(card_id, card_data, skill_data) -> PetInfo:
    # if card_id != 6596:
    #     return
    card_info = card_data[card_id]
    pet_info = PetInfo({
        'id': card_id,
        'name': card_info.name,
        'element': [card_info.element_id, card_info.sub_element_id],
        'type': [card_info.type_1_id, card_info.type_2_id, card_info.type_3_id],
        'rarity': card_info.rarity,
        'cost': card_info.cost,

        'max_level': card_info.max_level,
        'xp_type': card_info.xp_type,
        'xp_max': card_info.xp_curve().value_at(card_info.max_level),
        'params': {
            'hp_min': card_info.hp_min,
            'hp_max': card_info.hp_max,
            'hp_scale': card_info.hp_scale,

            'atk_min': card_info.atk_min,
            'atk_max': card_info.atk_max,
            'atk_scale': card_info.atk_scale,

            'rec_min': card_info.rec_min,
            'rec_max': card_info.rec_max,
            'rec_scale': card_info.rec_scale,
        },
        'awakenings': card_info.awakenings,
        'super_awakenings': card_info.super_awakenings,
        # 'active_skill': get_active_skill_detail(card_info.active_skill_id, skill_data),
        'leader_skill': get_leader_skill_detail(card_info.leader_skill_id, skill_data),
        'value': {
            'xp_per_level': card_info.feed_xp_per_level,
            'gold_per_level': card_info.sell_gold_per_level,
            'monster_point': card_info.sell_mp,
        },
        'base_id': card_info.base_id,
        'series_id': card_info.series_id,
        'collab_id': card_info.collab_id,
        'evo': {
            'is_ult': card_info.is_ult,
            'type': check_evo_type(card_info, card_data),  # 测试中
            'father_id': card_info.father_id,
            'mat': [card_info.evo_mat_id_1, card_info.evo_mat_id_2, card_info.evo_mat_id_3,
                    card_info.evo_mat_id_4, card_info.evo_mat_id_5],
        },
        'other': {
            'usable': card_info.assist_only_flag,
            'inheritable': card_info.inheritable,
            'take_assists': card_info.take_assists,
            'latent_slot_unlockable': card_info.latent_slot_unlock_flag,

            'is_collab': card_info.is_collab_flag,
            'stackable': card_info.is_stackable,
            'latent': card_info.latent_on_feed,

            'voice_id': card_info.voice_id,
            'orb_skin_id': card_info.orb_skin_id,
            'linked_id': card_info.linked_monster_no,
        },
        'search_text': card_info.search_text,
        'data_type': 'pet',
    })
    z = 1
    # print(pet_info['name'])

    return pet_info


# 进化类型
# 0: base
# 1: 进化
# 11: 究极进化
# 12: 超究极进化
# 21: 转生进化
# 22: 超转生进化
# 31: 点阵进化
# 41: 武装化
def check_evo_type(card_info, card_data):
    if len(card_info.awakenings) > 0 and card_info.awakenings[0] == 49:
        return EvoType.ASSIST  # 装备化
    if card_info.name.find('ドット・') == 0 and card_info.series_id != 500:  # 500是进化素材（点阵希石）
        return EvoType.DOT  # 点阵进化
    if card_info.base_id == card_info.id:
        return EvoType.BASE  # BASE卡
    father_info = card_data[card_info.father_id]
    if card_info.is_ult:
        if father_info.is_ult:
            return EvoType.SUPER_ULT  # 超究极进化
        else:
            return EvoType.ULT  # 究极进化
    else:
        if father_info.is_ult:
            return EvoType.REBIRTH  # 转生
        else:
            # 判断一下父级是否为转生
            if check_evo_type(father_info, card_data) == 21:
                return EvoType.SUPER_REBIRTH  # 超转生
            else:
                return EvoType.NORMAL  # 普通进化


# pet只包括玩家可用的卡
def get_pet_data() -> Dict[CardId, PetInfo]:
    card_data = load_card_data()
    skill_data = load_skill_data()

    pet_data = {}

    # 只需要玩家可用的卡
    for card_id in card_data.keys():
        if not card_data[card_id].ownable:
            continue
        pet_data[card_id] = clean_pet_info(card_id, card_data, skill_data)

    return pet_data
