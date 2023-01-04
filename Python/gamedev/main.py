import pyxel
from pyxelunicode import PyxelUnicode

pyuni = PyxelUnicode(r'D:\Github\Fragments\Python\gamedev\PixelMplus-20130602\PixelMplus12-Regular.ttf', 12)

class App:
    def __init__(self):
        pyxel.init(240, 240, fps=12, display_scale=2)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyuni.text(16, 16, '共和国の解体と再生')
        pyxel.show()
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)


if __name__ == "__main__":
    App()
    