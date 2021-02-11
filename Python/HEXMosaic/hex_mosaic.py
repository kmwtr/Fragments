#! python3
import os
import struct
import logging as log
from PIL import Image, ImageDraw

# Debug Setting
log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

# -------------------------------------------------

def check_sector_size(file_name: str, sector_size = 512) -> int:
    log.debug('-> check_sector_size()')

    size = os.path.getsize(file_name)
    sector_num = -(-size // sector_size)

    log.debug('size:   ' + str(size) + ' Byte')
    log.debug('sector: ' + str(sector_num) + ' Sector')

    return sector_num


def read_bytes(file_object, sector_size = 512, sector_offset = 0) -> int:
    #log.debug('-> read_bytes()')

    sector_offset *= sector_size
    file_object.seek(sector_offset)
    data = file_object.read(sector_size)

    #log.debug(data)

    num = int.from_bytes(data, 'big')

    # とりあえず今回は、何か有る／無いが知りたいので、これで良い。
    if num == 0:
        #log.debug('⬛')
        return 0
    else:
        #log.debug('⬜')
        return 1


def draw_image(pixel: list, whidth = 64):
    log.debug('-> draw_image()')

    height = -(-len(pixel) // whidth)

    amari = (height - (len(pixel) // whidth)) * whidth

    # 余り部分も作っておく
    #null_pixel = len(pixel) & whidth
    for i in range(amari):
        pixel.append(-1)

    log.debug('whidth: ' + str(whidth) +  ' height: ' + str(height))

    canvas_object = Image.new('RGB', (whidth, height), (0,0,255))
    draw = ImageDraw.Draw(canvas_object)

    for y in range(height):
        for x in range(whidth):
            color = pixel[(y * whidth) + x]
            if color is 0:
                draw.point((x, y), fill=(0, 0, 0))
            elif color is 1:
                draw.point((x, y), fill=(255, 255, 255))
            else:
                draw.point((x, y), fill=(0, 0, 255))
    
    # とりあえず2倍の画像にする
    canvas_object = canvas_object.resize((whidth * 2, height * 2), Image.NEAREST)
    canvas_object.save('hex_mosaic.png')

    return 0


def hex_mosaic():
    log.debug('-> hex_mosaic()')
    
    path = r'chinchillasystems_logo_mono.bin'

    file_object = open(path, 'rb')

    # 一旦「セクター」数を確認する
    sector_size = check_sector_size(path, 512) # ここもファイルオブジェクトにすべき。後で。

    # セクター数に応じてバイトの読み出しを繰り返す

    pixel = []
    for i in range(sector_size):
        pixel.append(read_bytes(file_object, 512, i))

    #log.debug(pixel)
    draw_image(pixel, 32)


# -------------------------------------------------

if __name__ is '__main__':
    hex_mosaic()
    #os.system('PAUSE')
