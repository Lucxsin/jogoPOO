
import arcade

from config import LARGURA, ALTURA
from classes.jogador import Player
from classes.vitamina import Vitamina
from classes.bacteria import Bacteria
from classes.antibiotico import Antibiotico
from classes.super_bacteria import SuperBacteria
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

        for i in range(25):
            self.vitamina_list.append(Vitamina())

        # Antibióticos
        self.antibiotico_list = arcade.SpriteList()

        for i in range(2):
            self.antibiotico_list.append(Antibiotico())

        # Bacteria
        self.bacteria_list = arcade.SpriteList()

        for i in range(3):
            self.bacteria_list.append(Bacteria())

        # Super bactéria
        self.super_bacteria_list = arcade.SpriteList()

        self.super_bacteria = SuperBacteria(self.player)
        self.super_bacteria_list.append(self.super_bacteria)

        # Pontuação
        self.pontos = 0

        self.tempo_jogo = 0

        # Tempo que o alerta "-1 ponto" ficará na tela
        self.alerta_tempo = 0

        self.colidindo_bacteria = False
        self.colidindo_super = False
        self.sofreu_dano = False


    def on_draw(self):

        self.clear()

        self.background_list.draw()
        self.vitamina_list.draw()
        self.antibiotico_list.draw()
        self.bacteria_list.draw()
        self.super_bacteria_list.draw()
        self.player_list.draw()

        arcade.draw_text(
            f"Pontuação: {self.pontos}",
            25,
            650,
            arcade.color.WHITE,
            22
        )

        minutos = int(self.tempo_jogo) // 60
        segundos = int(self.tempo_jogo) % 60

        arcade.draw_text(
            f"Tempo: {minutos:02}:{segundos:02}",
            700,
            660,
            arcade.color.WHITE,
            22
            )

        if self.alerta_tempo > 0:
            arcade.draw_text(
                "-1 PONTO!",
                LARGURA // 2,
                ALTURA - 40,
                arcade.color.WHITE,
                24,
                anchor_x="center"
    )
            
    def on_update(self, delta_time):

        # Atualiza o cronômetro
        self.tempo_jogo += delta_time

        self.player_list.update()
        self.bacteria_list.update()
        self.antibiotico_list.update()
        self.super_bacteria_list.update()


        # Coleta vitaminas
        vitaminas = arcade.check_for_collision_with_list(
            self.player,
            self.vitamina_list
        )

        for vitamina in vitaminas:
            vitamina.remove_from_sprite_lists()
            self.pontos += 1

        
        antibioticos = arcade.check_for_collision_with_list(
            self.player,
            self.antibiotico_list
        )

        for antibiotico in antibioticos:
            antibiotico.remove_from_sprite_lists()
            self.pontos += 5

        # Verifica se todas as vitaminas foram coletadas
        if len(self.vitamina_list) == 0 and len(self.antibiotico_list) == 0:
        
            game_over = GameOverView(
                self.pontos,
                self.tempo_jogo
            )
        
            self.window.show_view(game_over)
        
            return    
        
        

            
        # Colisão com bacterias
        bacterias = arcade.check_for_collision_with_list(
            self.player,
            self.bacteria_list
        )

        if len(bacterias) > 0:

            # Só perde ponto quando começa a colisão
            if not self.colidindo_bacteria:
                self.pontos -= 1
                self.alerta_tempo = 0.5
                self.colidindo_bacteria = True
                self.sofreu_dano = True

        else:
            # Quando o jogador sair da colisão,
            # poderá perder ponto novamente na próxima colisão
            self.colidindo_bacteria = False

        #Faz o alerta desaparecer
        if self.alerta_tempo > 0:
            self.alerta_tempo -= delta_time

        #colisão com super bactéria
        super_bacteria = arcade.check_for_collision_with_list(
            self.player,
            self.super_bacteria_list
        )

        if len(super_bacteria) > 0:

            if not self.colidindo_super:
                self.pontos -= 1
                self.colidindo_super = True
                self.sofreu_dano = True

                for inimigo in super_bacteria:
                        inimigo.teleportar()

        else:
            self.colidindo_super = False

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.mover_esquerda()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.mover_direita()

        elif key == arcade.key.UP or key == arcade.key.W:
            self.player.mover_cima()

        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.mover_baixo()

        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())


    def on_key_release(self, key, modifiers):

        if key in [arcade.key.LEFT, arcade.key.A]:
            self.player.parar_horizontal()

        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.player.parar_horizontal()

        elif key in [arcade.key.UP, arcade.key.W]:
            self.player.parar_vertical()

        elif key in [arcade.key.DOWN, arcade.key.S]:
            self.player.parar_vertical()