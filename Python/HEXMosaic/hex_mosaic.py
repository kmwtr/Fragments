#! python3
import os
import struct
import logging as log
from PIL import Image, ImageDraw, ImageColor

# Debug Setting
log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

# Resurrect 64
resurrect64_plus = [
    '#000000',
    '#2e222f', '#3e3546', '#625565', '#966c6c', '#ab947a', '#694f62', '#7f708a', '#9babb2',
    '#c7dcd0', '#ffffff', '#6e2727', '#b33831', '#ea4f36', '#f57d4a', '#ae2334', '#e83b3b', 
    '#fb6b1d', '#f79617', '#f9c22b', '#7a3045', '#9e4539', '#cd683d', '#e6904e', '#fbb954',
    '#4c3e24', '#676633', '#a2a947', '#d5e04b', '#fbff86', '#165a4c', '#239063', '#1ebc73',
    '#91db69', '#cddf6c', '#313638', '#374e4a', '#547e64', '#92a984', '#b2ba90', '#0b5e65',
    '#0b8a8f', '#0eaf9b', '#30e1b9', '#8ff8e2', '#323353', '#484a77', '#4d65b4', '#4d9be6',
    '#8fd3ff', '#45293f', '#6b3e75', '#905ea9', '#a884f3', '#eaaded', '#753c54', '#a24b6f',
    '#cf657f', '#ed8099', '#831c5d', '#c32454', '#f04f78', '#f68181', '#fca790', '#fdcbb0',
    '#000000'
    ]

color_palette = [
    '#000000',
    '#2e222f', '#694f62', '#6e2727', '#ae2334', '#7a3045', '#4c3e24', '#165a4c', '#313638', 
    '#0b5e65', '#323353', '#45293f', '#753c54', '#831c5d', '#3e3546', '#7f708a', '#b33831',
    '#e83b3b', '#9e4539', '#676633', '#239063', '#374e4a', '#0b8a8f', '#484a77', '#6b3e75',
    '#a24b6f', '#c32454', '#625565', '#9babb2', '#ea4f36', '#fb6b1d', '#cd683d', '#a2a947',
    '#1ebc73', '#547e64', '#0eaf9b', '#4d65b4', '#905ea9', '#cf657f', '#f04f78', '#966c6c',
    '#c7dcd0', '#f57d4a', '#f79617', '#e6904e', '#d5e04b', '#91db69', '#92a984', '#30e1b9', 
    '#4d9be6', '#a884f3', '#ed8099', '#f68181', '#ab947a', '#ffffff', '#f9c22b', '#fbb954',
    '#fbff86', '#cddf6c', '#b2ba90', '#8ff8e2', '#8fd3ff', '#eaaded', '#fca790', '#fdcbb0',
    '#000000'
    ]

# -------------------------------------------------

def check_sector_num(file_name: str, sector_size = 512) -> int:
    log.debug('-> check_sector_size()')

    file_size = os.path.getsize(file_name)
    sector_num = -(-file_size // sector_size)

    log.debug('Sector size (Byte):  ' + str(sector_size))
    log.debug('File size (Byte):    ' + str(file_size))
    log.debug('Sector num (Sector): ' + str(sector_num))

    return sector_num


def dump_sector(file_object, sector_size = 512, sector_offset = 0) -> int:
    #log.debug('-> dump_sector()')

    # 狙った部分をダンプする
    sector_offset *= sector_size
    file_object.seek(sector_offset)

    # 64 bit == 8 Byte (little endian) ずつ値を読み取る
    unit = sector_size // 8
    flag = 0
    for i in range(unit):
        long_num = int.from_bytes(file_object.read(8), byteorder='little', signed=False)
        
        # とりあえずこの方式で、セクターが 512Byte あるならば 1 + 64色作れる。（うーんとりあえず0は黒にした。）
        if long_num != 0:
            flag += 1

    #log.debug(flag)
    return flag


def draw_image(pixel: list, whidth = 64):
    log.debug('-> draw_image()')

    height = -(-len(pixel) // whidth)
    # 画像の欠けている部分
    amari = (whidth * height) - len(pixel)

    # 余り部分も作っておく
    # null_pixel = len(pixel) & whidth
    for i in range(amari):
        pixel.append(65)

    log.debug('whidth: ' + str(whidth) +  ' height: ' + str(height))

    canvas_object = Image.new('RGB', (whidth, height), (0,0,0))
    draw = ImageDraw.Draw(canvas_object)

    for y in range(height):
        for x in range(whidth):
            color_index = pixel[(y * whidth) + x]
            #draw.point((x, y), fill=ImageColor.getrgb(color_palette[color_index]))
            if color_index == 65:
                draw.point((x, y), fill=(255, 0, 0))
            elif color_index > 0:
                color_index = 127 + (color_index * 2)
                draw.point((x, y), fill=(color_index, color_index, color_index))
            
    # とりあえず2倍の画像にする
    canvas_object = canvas_object.resize((whidth * 2, height * 2), Image.NEAREST)
    canvas_object.save('hex_mosaic.png')

    return 0


def hex_mosaic(file_name: str):
    log.debug('-> hex_mosaic()')

    log.debug('File name: ' + str(file_name))
    
    # 一旦「セクター」数を確認する
    sector_num = check_sector_num(file_name, 512) # ここもファイルオブジェクトにすべき。後で。

    # セクター数に応じてバイトの読み出しを繰り返す
    file_object = open(file_name, 'rb')

    # 全部取っていく
    log.debug('-> dump_sector()')
    pixel = []
    for i in range(sector_num):
        pixel.append(dump_sector(file_object, 512, i))

    #log.debug(pixel)
    draw_image(pixel, 2000) # 512 B * 2000 = 1,024,000 = 1KiB

# -------------------------------------------------

if __name__ is '__main__':
    hex_mosaic(r"D:\Projects\HW_Stela\RK_Stela\Armbian_focal_wifi_nano_2102_buckup.img")
    #hex_mosaic('chinchillasystems_logo_mono.bin')
    #os.system('PAUSE')
