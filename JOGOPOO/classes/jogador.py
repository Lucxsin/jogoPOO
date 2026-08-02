import arcade

from config import LARGURA, ALTURA

VELOCIDADE = 5


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Carrega os sprites
        self.sprite_baixo = arcade.load_texture("sprites/gb_baixo.png")
        self.sprite_atras = arcade.load_texture("sprites/gb_atras.png")
        self.sprite_direita = arcade.load_texture("sprites/gb_direita.png")
        self.sprite_esquerda = arcade.load_texture("sprites/gb_esquerda.png")

        # Sprite inicial
        self.texture = self.sprite_baixo

        # Escala
        self.scale = 0.50

        # Posição inicial
        self.center_x = LARGURA // 2
        self.center_y = ALTURA // 2

    def mover_esquerda(self):
        self.change_x = -VELOCIDADE
        self.texture = self.sprite_esquerda

    def mover_direita(self):
        self.change_x = VELOCIDADE
        self.texture = self.sprite_direita

    def mover_cima(self):
        self.change_y = VELOCIDADE
        self.texture = self.sprite_atras

    def mover_baixo(self):
        self.change_y = -VELOCIDADE
        self.texture = self.sprite_baixo

    def parar_horizontal(self):
        self.change_x = 0

    def parar_vertical(self):
        self.change_y = 0

    def update(self, delta_time=0):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Limites da tela
        if self.left < 0:
            self.left = 0

        if self.right > LARGURA:
            self.right = LARGURA

        if self.bottom < 0:
            self.bottom = 0

        if self.top > ALTURA:
            self.top = ALTURA