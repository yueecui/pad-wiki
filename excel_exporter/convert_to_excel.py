import os
from typing import List, Any, Optional
from danteng_lib import load_json
from SaveToExcel import save_to_excel
from excel_exporter.header import CARD_DATA_HEADER, SKILL_DATA_HEADER

BASE_PATH = 'raw_data'
OUTPUT_PATH = 'excel'
CARD_DATA_FILENAME = 'download_card_data.json'
SKILL_DATA_FILENAME = 'download_skill_data.json'


def _unflatten(raw: List[Any], idx: int, width: int, replace: bool = False):
    """Unflatten a card array.

    Index is the slot containing the item count.
    Width is the number of slots per item.
    If replace is true, values are moved into an array at idx.
    If replace is false, values are deleted.
    """
    item_count = raw[idx]
    if item_count == 0:
        if replace:
            raw[idx] = list()
            return

    data_start = idx + 1
    flattened_item_count = width * item_count
    flattened_data_slice = slice(data_start, data_start + flattened_item_count)

    data = list(raw[flattened_data_slice])
    del raw[flattened_data_slice]

    if replace:
        raw[idx] = data


def export_card_data() -> None:
    raw_card_data = load_json(os.path.join(BASE_PATH, CARD_DATA_FILENAME))

    # 生成excel数据
    sheet_name = 'CARD_DATA'
    headers = {
        sheet_name: []
    }
    contents = {
        sheet_name: {}
    }

    for card_info in raw_card_data['card']:
        _unflatten(card_info, 57, 3, replace=True)
        _unflatten(card_info, 58, 1, replace=True)

        card_info_dict = {}
        for index in range(0, len(card_info)):
            key = CARD_DATA_HEADER[index]
            if key not in headers[sheet_name]:
                headers[sheet_name].append(key)
            card_info_dict[key] = card_info[index]
        contents[sheet_name][card_info[0]] = card_info_dict

    save_filepath = os.path.join(OUTPUT_PATH, CARD_DATA_FILENAME + '.xlsx')
    save_to_excel(headers, contents, save_filepath)


def export_skill_data() -> None:
    raw_skill_data = load_json(os.path.join(BASE_PATH, SKILL_DATA_FILENAME))

    # 生成excel数据
    sheet_name = 'SKILL_DATA'
    headers = {
        sheet_name: ['编号']
    }
    contents = {
        sheet_name: {}
    }

    for i, skill_info in enumerate(raw_skill_data['skill']):
        skill_info_dict = {}
        for index in range(0, len(skill_info)):
            key = SKILL_DATA_HEADER[index] if len(SKILL_DATA_HEADER) > index else str(index)
            if key not in headers[sheet_name]:
                headers[sheet_name].append(key)
            skill_info_dict[key] = skill_info[index]
            skill_info_dict['编号'] = i
        contents[sheet_name][i] = skill_info_dict

    save_filepath = os.path.join(OUTPUT_PATH, SKILL_DATA_FILENAME + '.xlsx')
    save_to_excel(headers, contents, save_filepath)


if __name__ == '__main__':
    export_card_data()
    export_skill_data()
