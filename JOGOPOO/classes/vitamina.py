import arcade
import random

from config import LARGURA, ALTURA


class Vitamina(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "sprites/vitamina.png",
            scale=0.18
        )

        self.center_x = random.randint(40, LARGURA - 40)
        self.center_y = random.randint(40, ALTURA - 40)