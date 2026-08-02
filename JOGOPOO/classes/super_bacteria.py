import arcade
import random
import math

from config import LARGURA, ALTURA


class SuperBacteria(arcade.Sprite):

    def __init__(self, player):
        super().__init__(
            "sprites/super_bacteria.png",
            scale=0.12
        )

        self.player = player
        self.velocidade = 2

        self.teleportar()

    def teleportar(self):

        while True:

            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)

            distancia = math.sqrt(
                (x - self.player.center_x) ** 2 +
                (y - self.player.center_y) ** 2
            )

            if distancia > 250:
                self.center_x = x
                self.center_y = y
                break

    def update(self, delta_time=0):

        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y

        distancia = math.sqrt(dx**2 + dy**2)

        if distancia != 0:
            self.center_x += (dx / distancia) * self.velocidade
            self.center_y += (dy / distancia) * self.velocidade