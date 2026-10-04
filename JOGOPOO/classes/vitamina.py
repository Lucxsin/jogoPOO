import arcade


class Vitamina(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(
            "sprites/vitamina.png",
            scale=0.08
        )

        # A posição agora é escolhida pela GameView (em cima das plataformas)
        self.center_x = x
        self.center_y = y