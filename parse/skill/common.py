ELEMENT_MAP = {
    0: '火',
    1: '水',
    2: '木',
    3: '光',
    4: '暗',
}

DROP_MAP = {
    0: '火',
    1: '水',
    2: '木',
    3: '光',
    4: '暗',
    5: '回复',
    6: '废',
    7: '毒',
}


def element(element_id):
    return f'{ELEMENT_MAP[element_id]}属性'


def drop_buff(drop_id):
    assert 0 <= drop_id <= 5
    if drop_id == 5:
        return '回复力'
    else:
        return f'{ELEMENT_MAP[drop_id]}属性攻击力'

def drop(drop_id):
    return f'{DROP_MAP[drop_id]}宝珠'