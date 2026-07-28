import arcade

from config import LARGURA, ALTURA
from classes.jogador import Player  


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Lista de sprites do cenário
        self.background_list = arcade.SpriteList()

        # Sprite do cenário
        background = arcade.Sprite("sprites/cenario.jpg")

        #Centraliza o cenário na tela
        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2

        #Ajusta o tamanho do cenário para preencher a tela
        background.width = LARGURA
        background.height = ALTURA

        # Adiciona o cenário na lista
        self.background_list.append(background)

       # Lista do jogador
        self.player_list = arcade.SpriteList()

        # Cria o jogador
        self.player = Player()

        # Adiciona na lista
        self.player_list.append(self.player)

    def on_draw(self):

        self.clear()

        self.background_list.draw()

        self.player_list.draw()

       

    def on_update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.player.mover_esquerda()

        elif key == arcade.key.RIGHT:
            self.player.mover_direita()

        elif key == arcade.key.UP:
            self.player.mover_cima()

        elif key == arcade.key.DOWN:
            self.player.mover_baixo()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.parar_horizontal()

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.parar_vertical()

    