import arcade
import random
import math

from config import LARGURA, ALTURA


class Vitamina(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "sprites/vitamina.png",
            scale=0.08
        )

        while True:

            x = random.randint(80, LARGURA - 80)
            y = random.randint(80, ALTURA - 80)

            distancia = math.sqrt(
                (x - LARGURA / 2) ** 2 +
                (y - ALTURA / 2) ** 2
            )

            if distancia > 180:
                self.center_x = x
                self.center_y = y
                break