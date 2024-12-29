import random
from candy import Candy

class Board:
    """
    This class represents the board of the game. It is a 2D array of cells.
    """

    def __init__(self):
        # セルの中身を0~4のランダムな数字で埋める
        cells: list[int] = [random.randint(0, 3) for _ in range(50)]

        # キャンディのリストを初期化
        self.candy_cells: list[Candy] = []
        for i, cell in enumerate(cells):
            x = i % 10
            y = i // 10
            candy = Candy(
                size=16,
                x=x,
                y=y,
                resource_bank=0,
                resource_x=cell * 16,
                resource_y=0,
                transparent_color=0
            )
            self.candy_cells.append(candy)

    def swap(self, index1: int, index2: int):
        """
        キャンディをスワップする
        """
        self.candy_cells[index1], self.candy_cells[index2] = self.candy_cells[index2], self.candy_cells[index1]
