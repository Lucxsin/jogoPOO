import arcade

from config import LARGURA, ALTURA
from classes.jogador import Player
from classes.vitamina import Vitamina


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Fundo
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite("sprites/cenario.jpg")
        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2
        background.width = LARGURA
        background.height = ALTURA

        self.background_list.append(background)

        # Jogador
        self.player_list = arcade.SpriteList()

        self.player = Player()
        self.player_list.append(self.player)

        # Vitaminas
        self.vitamina_list = arcade.SpriteList()

        for i in range(6):

            while True:
                vitamina = Vitamina()

                # Só adiciona se não estiver encostando no jogador
                if not arcade.check_for_collision(vitamina, self.player):
                    self.vitamina_list.append(vitamina)
                    break

        # Pontuação
        self.pontos = 0

    def on_draw(self):

        self.clear()

        self.background_list.draw()

        self.vitamina_list.draw()

        self.player_list.draw()

        arcade.draw_text(
            f"Vitaminas: {self.pontos}",
            20,
            560,
            arcade.color.WHITE,
            20
        )

    def on_update(self, delta_time):

        self.player_list.update()

        vitaminas = arcade.check_for_collision_with_list(
            self.player,
            self.vitamina_list
        )

        for vitamina in vitaminas:
            vitamina.remove_from_sprite_lists()
            self.pontos += 1

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