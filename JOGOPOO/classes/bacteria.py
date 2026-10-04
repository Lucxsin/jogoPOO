import arcade
import random
import math

from config import LARGURA, ALTURA, SPAWN_X, SPAWN_Y


class Bacteria(arcade.Sprite):

    def __init__(self):
        super().__init__(
            "sprites/virus.png",
            scale=0.10
        )

        while True:
            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)

            distancia = math.sqrt(
                (x - LARGURA / 2) ** 2 +
                (y - ALTURA / 2) ** 2
            )

             # Só aceita posições longe do jogador
            if distancia > 200:
                self.center_x = x
                self.center_y = y
                break


        self.change_x = random.choice([-2.5, 2.5])
        self.change_y = random.choice([-2.5, 2.5])

    def update(self, delta_time=0):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left <= 0 or self.right >= LARGURA:
            self.change_x *= -1

        if self.bottom <= 0 or self.top >= ALTURA:
            self.change_y *= -1