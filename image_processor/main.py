import os
from config import IMAGE_BASE_PATH, IMAGE_RAW_PATH
from image_processor.dowload_image import download_all_card_bc
from image_processor.PADTextureTool import TextureReader, TextureWriter, PVRTC2BPP, PVRTC4BPP
from parse.raw.card import load_card_data
from shutil import copyfile


def update_cards_image():
    # 更新cards
    need_update_list = download_all_card_bc()

    if len(need_update_list) > 0:
        image_type = 'cards'

        raw_base_path = os.path.join(IMAGE_BASE_PATH, IMAGE_RAW_PATH, image_type)
        for assets in need_update_list:
            file_full_path = os.path.join(raw_base_path, assets.file_name)
            with open(file_full_path, 'rb') as binaryFile:
                file_contents = binaryFile.read()

            textures = list(TextureReader.extractTexturesFromBinaryBlob(file_contents, file_full_path))

            output_base_path = os.path.join(IMAGE_BASE_PATH, image_type)
            for texture in textures:
                output_filename = texture.name
                output_file_full_path = os.path.join(output_base_path, output_filename)

                if texture.encoding in [PVRTC2BPP, PVRTC4BPP]:
                    print(f"Warning: {output_filename} is encoded using PVR texture compression. This format is not yet supported by the Puzzle & Dragons Texture Tool.")
                TextureWriter.exportToImageFile(texture, output_file_full_path)
                print(f"{output_filename} ({texture.width} x {texture.height}）已保存")


def generate_monster_icon():
    card_data = load_card_data()

    for card_id, card_info in card_data.items():
        if not card_info.ownable:
            continue
        icon_info = get_monster_icon_info(card_info)
        if not os.path.exists(icon_info['path']):
            os.makedirs(icon_info['path'])

        if not os.path.exists(icon_info['full_path']):
            cmd = f'image/convert.exe -size 98x99 xc:"rgba(0,0,0,0)" ' \
                  f'-size 92x92 xc:"rgba(68,68,68,1)" -geometry 92x92+3+3 -composite ' \
                  f'( -crop 96x96+{icon_info["offset"][0]}+{icon_info["offset"][1]} image/cards/{icon_info["card_file"]} ) -geometry 96x96+1+1 -composite ' \
                  f'image/cf_{icon_info["ele1"]}.png -composite ' \
                  f'{"image/sub_cf_%d.png -composite " % icon_info["ele2"] if icon_info["ele2"] > -1 else ""}' \
                  f'{icon_info["full_path"]}'
            cmd = cmd.replace('/', '\\')
            z = 1
            if os.system(cmd):
                print(f'图片[{icon_info["file_name"]}]保存出错！请检查！')
            else:
                copyfile(icon_info['full_path'], os.path.join('upload', icon_info['file_name']))
                print(f'图片[{icon_info["file_name"]}]保存完成！')



def get_monster_icon_info(card_info):
    folder = '%04d' % int((card_info.id-1) / 1000)
    path = os.path.join(IMAGE_BASE_PATH, 'pet_icon', folder)
    file_name = 'pet_%04d.png' % card_info.id
    full_path = os.path.join(path, file_name)
    return {
        'id': card_info.id,
        'card_file': 'CARDS_%03d.PNG' % (int((card_info.id-1) / 100)+1),
        'offset': [
            (card_info.id - 1) % 10 * (96 + 6),
            (int((card_info.id - 1) / 10) % 10) * (96 + 6)
        ],
        'path': path,
        'file_name': file_name,
        'full_path': full_path,
        'ele1': card_info.element_id,
        'ele2': card_info.sub_element_id,
    }




if __name__ == '__main__':
    # update_cards_image()
    generate_monster_icon()

