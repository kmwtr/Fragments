import pyxel
import PyxelUniversalFont as puf

writer = puf.Writer("misaki_gothic.ttf")

class App:
    def __init__(self):
        pyxel.init(240, 240, fps=12, display_scale=2)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        writer.draw(16, 16, '共和国の解体と再生', 16, 2)
        pyxel.rect(0, 0, 16, 16, 1)
        pyxel.show()
        pyxel.cls(0)


if __name__ == "__main__":
    App()
    