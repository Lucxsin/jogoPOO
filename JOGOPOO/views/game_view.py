
import arcade

from config import LARGURA, ALTURA
from classes.jogador import Player
from classes.vitamina import Vitamina
from classes.bacteria import Bacteria
from views.game_over_view import GameOverView


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
            self.vitamina_list.append(Vitamina())

        # Vírus
        self.bacteria_list = arcade.SpriteList()

        for i in range(3):
            self.bacteria_list.append(Bacteria())

        # Pontuação
        self.pontos = 0

        # Vida
        self.vida = 100

    def on_draw(self):

        self.clear()

        self.background_list.draw()
        self.vitamina_list.draw()
        self.bacteria_list.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Pontuação: {self.pontos}",
            20,
            560,
            arcade.color.WHITE,
            20
        )

        arcade.draw_text(
            f"Vida: {self.vida}%",
            20,
            530,
            arcade.color.LIME_GREEN,
            20
        )

    def on_update(self, delta_time):

        self.player_list.update()
        self.bacteria_list.update()

        # Coleta vitaminas
        vitaminas = arcade.check_for_collision_with_list(
            self.player,
            self.vitamina_list
        )

        for vitamina in vitaminas:

            vitamina.remove_from_sprite_lists()

            self.pontos += 1

            # Cria outra vitamina
            self.vitamina_list.append(Vitamina())

        # Colisão com vírus
        virus = arcade.check_for_collision_with_list(
            self.player,
            self.bacteria_list
        )

        if len(virus) > 0:

            self.vida -= 50

            for bacteria in virus:
                bacteria.remove_from_sprite_lists()

                # Cria outro vírus
                self.bacteria_list.append(Bacteria())

            if self.vida <= 0:
                self.window.show_view(GameOverView())

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