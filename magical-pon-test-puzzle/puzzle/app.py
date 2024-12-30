import pyxel # type: ignore

from board import Board
from candy import Candy


class App:
    def __init__(self):
        """初期化処理
        """
        # Pyxelの初期化
        pyxel.init(width=160, height=120)
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)

        # ボードの初期化
        self.board = Board()

        # キャンディの選択状態を管理する変数
        self.selected_candy: Candy = None  # クリックされたキャンディを追跡する変数
        self.selected_candy_offset_x = 0
        self.selected_candy_offset_y = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム更新処理
        """

        # マウスがクリックされたときの処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.on_mouse_down(pyxel.mouse_x, pyxel.mouse_y)

        # マウスのクリックが離されたときの処理
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.on_mouse_up(pyxel.mouse_x, pyxel.mouse_y)

        # キャンディが選択されている場合の処理
        if self.selected_candy:
            # マウスの位置にキャンディを追従させる
            self.selected_candy.x = pyxel.mouse_x - self.selected_candy_offset_x
            self.selected_candy.y = pyxel.mouse_y - self.selected_candy_offset_y


    def draw(self):
        """フレーム描画処理
        """

        # 画面をクリア
        pyxel.cls(0)

        # ボードの描画
        self.draw_board()

        # 選択されたキャンディの描画
        self.draw_selected_candy()

        # カーソルの描画
        self.draw_cursor()

    def draw_board(self):
        """ボードの描画処理
        """
        # ボードのキャンディを描画
        for i, candy in enumerate(self.board.candy_cells):
            candy.draw()

    def draw_selected_candy(self):
        """選択されたキャンディの描画処理
        """
        if self.selected_candy != None:
            pyxel.blt(
                self.selected_candy.x,
                self.selected_candy.y,
                0,
                0,
                self.selected_candy.resource_x,
                self.selected_candy.resource_y,
                self.selected_candy.size,
                self.selected_candy.size
            )

            print(self.selected_candy.x, self.selected_candy.y)

    def draw_cursor(self):
        """カーソルの描画処理
        """
        x = pyxel.mouse_x // 16
        y = pyxel.mouse_y // 16
        pyxel.rectb(x * 16, y * 16, 16, 16, 7)

    def on_mouse_down(self, x: int, y: int):
        """マウスがクリックされたときの処理"""

        for candy in self.board.candy_cells:
            if candy.x <= x < candy.x + candy.size and candy.y <= y < candy.y + candy.size:
                self.selected_candy = candy
                self.selected_candy_offset_x = x - candy.x
                self.selected_candy_offset_y = y - candy.y
                break

    def on_mouse_up(self, x: int, y: int):
        """マウスのクリックが離されたときの処理"""

        for candy in self.board.candy_cells:
            if candy.x <= x < candy.x + candy.size and candy.y <= y < candy.y + candy.size:

                # 選択中のキャンディをグリッドにスナップさせる
                self.selected_candy.x = self.selected_candy.x // 16 * 16
                self.selected_candy.y = self.selected_candy.y // 16 * 16

                # クリックが離されたキャンディをグリッドにスナップさせる
                candy.x = candy.x // 16 * 16
                candy.y = candy.y // 16 * 16

                # 選択中のキャンディとクリックが離されたキャンディを入れ替える
                self.board.swap(
                    self.board.candy_cells.index(self.selected_candy),
                    self.board.candy_cells.index(candy))

                self.selected_candy = None
                break


App()