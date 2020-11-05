# 整理card数据
from typing import Dict, Any
from common.pad_types import CardId, PetInfo
from parse.raw.skill import load_skill_data
from parse.raw.card import load_card_data


def clean_pet_info(card_info, skill_data) -> PetInfo:
    pet_info = PetInfo({})
    z = 1

    return pet_info


# pet只包括玩家可用的卡
def get_pet_data() -> Dict[CardId, PetInfo]:
    card_data = load_card_data()
    skill_data = load_skill_data()

    pet_data = {}

    # 只需要玩家可用的卡
    for card_id, card_info in card_data.items():
        if not card_info.ownable:
            continue
        pet_data[card_id] = clean_pet_info(card_info, skill_data)

    return pet_data
