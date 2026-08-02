import arcade
import random
import math

from config import LARGURA, ALTURA


class Antibiotico(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "sprites/antibiotico.png",
            scale=0.13
        )

        # Nasce longe do jogador
        while True:

            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)

            distancia = math.sqrt(
                (x - LARGURA / 2) ** 2 +
                (y - ALTURA / 2) ** 2
            )

            if distancia > 180:
                self.center_x = x
                self.center_y = y
                break

        # Movimento inicial
        self.change_x = random.choice([-2, 2])
        self.change_y = random.choice([-2, 2])

    def update(self, delta_time=0):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Rebote nas paredes
        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1

        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1