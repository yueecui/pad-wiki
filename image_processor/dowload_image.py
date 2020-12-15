import padtools
import os
from config import IMAGE_BASE_PATH, IMAGE_RAW_PATH
from danteng_downloader import Downloader


def download_all_card_bc():
    pad_jp = padtools.regions.japan.server
    downloader = Downloader()

    need_update_list = []
    for assets in pad_jp.assets:
        if check_file_name_prefix(assets.file_name, 'cards_'):
            if download_bc(downloader, assets, 'cards'):
                need_update_list.append(assets)
    downloader.wait_threads()
    return need_update_list


def check_file_name_prefix(filename, prefix):
    return bool(len(filename) > len(prefix) and filename.find(prefix) == 0)


def download_bc(downloader, assets, path):
    save_path = os.path.join(IMAGE_BASE_PATH, IMAGE_RAW_PATH, path)
    file_full_path = os.path.join(save_path, assets.file_name)
    if os.path.exists(file_full_path) and os.path.getsize(file_full_path) == assets.compressed_size:
        return False
    downloader.download(assets.url, save_path, assets.file_name)
    return True

