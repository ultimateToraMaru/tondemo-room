import pyxel # type: ignore

class Candy:
    """
    This class represents a candy object.
    """
    def __init__(self, size: int, x: int, y: int, resource_bank: int, resource_x: int, resource_y: int, transparent_color: int):
        self.size: int = size
        self.x: int = x
        self.y: int = y
        self.resource_bank: int = resource_bank
        self.resource_x: int = resource_x
        self.resource_y: int = resource_y
        self.transparent_color: int =  transparent_color

    def draw(self):
        pyxel.blt(
            # 描画位置
            self.x,
            self.y,

            # リソースのバンク
            self.resource_bank,

            # リソースの位置
            self.resource_x,
            self.resource_y,

            # リソースのサイズ
            self.size,
            self.size,

            # 透明色
            self.transparent_color,

            # 反転
            0,

            # 倍率
            1
        )