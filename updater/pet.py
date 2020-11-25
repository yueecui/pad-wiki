import json
import os
from parse.pet_data import get_all_pet_data
from huijiWiki import HuijiWiki
from config import WIKITEXT_PATH
from config_loader import config_loader


def update_all_data():
    # 读取配置文件
    cfg = config_loader('config.ini')

    pad_wiki = login_in_wiki(cfg)
    update_pet_data(pad_wiki)


def update_pet_data(pad_wiki):
    pet_data = get_all_pet_data()
    show_page_update_list = []

    # 生成数据
    for pet_id, pet_info in pet_data.items():
        # 控制上传部分
        data_page_title = 'Data:Pet/%04d.json' % pet_id
        data_page_content = json.dumps(pet_info, ensure_ascii=False)
        data_page_savepath = os.path.join(WIKITEXT_PATH, '%s.txt' % HuijiWiki.filename_fix(data_page_title))

        # page_title = 'Pet/%04d' % pet_id
        # page_content = '{{PetPage}}' % pet_id
        # page_savepath = os.path.join(WIKITEXT_PATH, '%s.txt' % HuijiWiki.filename_fix(page_title))
        # saved_page_content, read_result = read_file(page_savepath)
        # if not read_result or saved_page_content != page_content:
        #     show_page_update_list.append(OrderedDict([
        #         ('title', page_title),
        #         ('content', page_content),
        #         ('save_path', page_savepath),
        #     ]))

        # 更新页面
        pad_wiki.edit(data_page_title, data_page_content, filepath=data_page_savepath, compare_flag=True)
    pad_wiki.wait_threads()
    return show_page_update_list


def login_in_wiki(cfg):
    # 更新数据的话，先登录wiki
    pad_wiki = HuijiWiki('pad', 'PADWIKI')
    if not pad_wiki.login(cfg['WIKI']['username'], cfg['WIKI']['password']):
        print('登录失败')
        return
    if not pad_wiki.get_edit_token():
        print('获取token失败')
        return
    # 设置线程数
    pad_wiki.set_thread_number(cfg['WIKI'].get('thread_number') or 10)
    pad_wiki.set_sleep_time(cfg['WIKI'].get('sleep_time') or 3)

    return pad_wiki


if __name__ == '__main__':
    update_all_data()

