import arcade

from config import LARGURA, ALTURA, VELOCIDADE_JOGADOR


class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Carrega as texturas
        self.baixo = arcade.load_texture("sprites/gb_baixo.png")
        self.cima = arcade.load_texture("sprites/gb_atras.png")
        self.esquerda = arcade.load_texture("sprites/gb_esquerda.png")
        self.direita = arcade.load_texture("sprites/gb_direita.png")

        # Textura inicial
        self.texture = self.baixo

        # Posição inicial
        self.center_x = LARGURA / 2
        self.center_y = ALTURA / 2

        # Velocidade inicial
        self.velocidade = VELOCIDADE_JOGADOR

    #MOVIMENTO

    def mover_esquerda(self):
        self.change_x = -self.velocidade
        self.texture = self.esquerda

    def mover_direita(self):
        self.change_x = self.velocidade
        self.texture = self.direita

    def mover_cima(self):
        self.change_y = self.velocidade
        self.texture = self.cima

    def mover_baixo(self):
        self.change_y = -self.velocidade
        self.texture = self.baixo

    #PARAR
    def parar_horizontal(self):
        self.change_x = 0

    def parar_vertical(self):
        self.change_y = 0

    # Atualiza a posição do jogador
    def update(self, delta_time):
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

