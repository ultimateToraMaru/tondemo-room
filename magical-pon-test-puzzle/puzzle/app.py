import pyxel # type: ignore

from board import Board

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

        pyxel.run(self.update, self.draw)

    def update(self):
        """フレーム更新処理
        """

        # マウスがクリックされたときの処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x // 16
            y = pyxel.mouse_y // 16

            self.on_mouse_down(x, y, 0)

        # マウスのクリックが離されたときの処理
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x // 16
            y = pyxel.mouse_y // 16

            self.on_mouse_up(x, y, 0)

    def draw(self):
        """フレーム描画処理
        """
        pyxel.cls(0)
        self.draw_board()
        self.draw_cursor()

    def draw_board(self):
        """ボードの描画処理
        """

        # ボードのキャンディを描画
        for i, candy in enumerate(self.board.candy_cells):
            candy.draw()

    def draw_cursor(self):
        """カーソルの描画処理
        """
        x = pyxel.mouse_x // 16
        y = pyxel.mouse_y // 16
        pyxel.rectb(x * 16, y * 16, 16, 16, 7)

    def on_mouse_down(self, x: int, y: int, button: int):
        """マウスがクリックされたときの処理
        """
        print("down "f"({x}, {y})")
        self.pick_candy(x, y)

    def on_mouse_up(self, x: int, y: int, button: int):
        """マウスのクリックが離されたときの処理
        """
        print("up "f"({x}, {y})")

    def pick_candy(self, x: int, y: int):
        """キャンディを選択する
        """
        pass

    def swipe

App()