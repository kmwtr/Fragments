#! python3
import logging as log
import os
import sys
import subprocess

import debug_config

def run_mozjpg(file_path: str, output_dir: str):
    log.debug('> def ' + sys._getframe().f_code.co_name)

    # cjpeg
    # 圧縮、中間ファイルとして出力
    mozjpeg_command = ['cjpeg', '-quality', '90', '-outfile', 'intermediate_img.jpg', file_path]
    cp = subprocess.run(mozjpeg_command, encoding='utf-8', stdout=subprocess.PIPE)
    log.debug(cp)

    # jpegtran
    # Exif 等メタデータを削除、最終ファイル出力
    target_path = os.path.join(output_dir, 'intermediate_img.jpg')
    jpegtran_command = ['jpegtran', '-copy', 'none', '-outfile', 'final.jpg', target_path]
    cp = subprocess.run(jpegtran_command, encoding='utf-8', stdout=subprocess.PIPE)
    log.debug(cp)

    # 中間ファイル削除
    os.remove('intermediate_img.jpg')

# -------------------------------------------------

if __name__ == '__main__':
    run_mozjpg('image.png', '')