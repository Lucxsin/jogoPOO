import arcade
import random

from config import LARGURA, ALTURA


class Bacteria(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "sprites/virus.png",
            scale=0.20
        )

        self.center_x = random.randint(100, LARGURA - 100)
        self.center_y = random.randint(100, ALTURA - 100)

        self.change_x = random.choice([-3, 3])
        self.change_y = random.choice([-3, 3])

    def update(self, delta_time=0):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1

        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1