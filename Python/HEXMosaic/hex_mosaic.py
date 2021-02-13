#! python3
import os
import struct
import logging as log
from PIL import Image, ImageDraw, ImageColor

# Debug Setting
log.basicConfig(level=log.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')

heatmap = [
    '#000000',
    '#142966', '#152a67', '#152b68', '#152e6a', '#152f6b', '#15326d', '#15356f', '#153872',
    '#153b74', '#154078', '#16447b', '#16497f', '#164e83', '#175387', '#18588a', '#185d8e',
    '#1a6291', '#1b6794', '#1d6c97', '#1f729a', '#22769b', '#257c9e', '#2881a0', '#2b86a1',
    '#2f8ca3', '#3491a4', '#3897a4', '#3d9ca4', '#42a1a4', '#48a6a4', '#4daba4', '#54afa4',
    '#5ab3a3', '#5fb6a1', '#67b99e', '#6fbc99', '#78bf94', '#81c28e', '#8bc488', '#94c682', 
    '#9dc87c', '#a6ca76', '#adcb72', '#b5cb6d', '#bdcc69', '#c2cc67', '#cccb66', '#d3c766', 
    '#dac266', '#e0bc66', '#e5b666', '#e9b166', '#eeb066', '#f1b06b', '#f4b372', '#f6b97a',
    '#f8c388', '#f9cd93', '#f9d79e', '#fae1aa', '#faeab4', '#faf0bb', '#faf8c4', '#fbfcc8',
    '#ff0000'
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
            draw.point((x, y), fill=ImageColor.getrgb(heatmap[color_index]))
            '''
            if color_index == 65:
                draw.point((x, y), fill=(255, 0, 0))
            elif color_index > 0:
                color_index = 127 + (color_index * 2)
                draw.point((x, y), fill=(color_index, color_index, color_index))
                '''
            
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
    #os.system('PAUSE')
