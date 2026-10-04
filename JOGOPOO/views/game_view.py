import arcade

import random

from config import (
    LARGURA,
    ALTURA,
    GRAVIDADE,
    FORCA_PULO,
    TAMANHO_BLOCO,
    SPAWN_X,
)
from classes.jogador import Player
from classes.bloco import Bloco
from classes.vitamina import Vitamina
from classes.bacteria import Bacteria
from classes.antibiotico import Antibiotico
from classes.super_bacteria import SuperBacteria
from views.game_over_view import GameOverView


# Mapa da fase: cada linha tem 18 colunas de 50 px (900 px de largura).
# '#' = bloco | '.' = vazio. A primeira linha é o topo da tela.
MAPA = [
    "..................",
    "..................",
    "..................",
    "..................",
    ".####........####.",   # plataformas altas
    "..................",
    "..................",
    ".......####.......",   # plataforma do meio
    "..................",
    "..................",
    ".#####......#####.",   # plataformas baixas
    "..................",
    "..................",
    "##################",   # chão
]


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
        self.player.center_x = SPAWN_X
        self.player.bottom = TAMANHO_BLOCO      # em cima do chão
        self.player_list.append(self.player)

        # Cenário: chão e plataformas (lista de Blocos)
        self.bloco_list = arcade.SpriteList()
        self.construir_mapa()

        # Motor de física: gravidade + colisão do jogador com os blocos
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.bloco_list,
            gravity_constant=GRAVIDADE
        )

        # Teclas de movimento que estão pressionadas agora
        self.tecla_esquerda = False
        self.tecla_direita = False

        # Vitaminas
        self.vitamina_list = arcade.SpriteList()

        for x, y in self.sortear_posicoes_vitaminas(25):
            self.vitamina_list.append(Vitamina(x, y))

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


    def construir_mapa(self):
        """Lê o MAPA e cria um Bloco para cada '#'."""
        total_linhas = len(MAPA)

        for linha, texto in enumerate(MAPA):
            for coluna, caractere in enumerate(texto):
                if caractere == "#":
                    x = coluna * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
                    y = (total_linhas - 1 - linha) * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
                    self.bloco_list.append(Bloco(x, y))

    def sortear_posicoes_vitaminas(self, quantidade):
        """Sorteia posições livres em cima dos blocos (longe de onde o jogador nasce)."""
        total_linhas = len(MAPA)
        candidatas = []

        for linha, texto in enumerate(MAPA):
            for coluna, caractere in enumerate(texto):
                # só vale se for bloco e o espaço acima dele estiver vazio
                if caractere != "#" or linha == 0 or MAPA[linha - 1][coluna] != ".":
                    continue

                x = coluna * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
                topo = (total_linhas - linha) * TAMANHO_BLOCO

                if abs(x - SPAWN_X) < 100 and topo == TAMANHO_BLOCO:
                    continue    # não nasce em cima do jogador

                candidatas.append((x, topo + 28))

        return random.sample(candidatas, quantidade)

    def atualizar_movimento(self):
        """Define a velocidade horizontal conforme as teclas pressionadas."""
        if self.tecla_esquerda and not self.tecla_direita:
            self.player.mover_esquerda()
        elif self.tecla_direita and not self.tecla_esquerda:
            self.player.mover_direita()
        else:
            self.player.parar_horizontal()

    def on_draw(self):

        self.clear()

        self.background_list.draw()
        self.bloco_list.draw()
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

        # Física primeiro (move o jogador), depois a animação
        self.physics_engine.update()
        self.player.update(delta_time)

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
            self.tecla_esquerda = True
            self.atualizar_movimento()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.tecla_direita = True
            self.atualizar_movimento()

        elif key in [arcade.key.UP, arcade.key.W, arcade.key.SPACE]:
            # can_jump() bloqueia o pulo duplo: só pula se estiver no chão
            if self.physics_engine.can_jump():
                self.player.change_y = FORCA_PULO

        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())


    def on_key_release(self, key, modifiers):

        if key in [arcade.key.LEFT, arcade.key.A]:
            self.tecla_esquerda = False
            self.atualizar_movimento()

        elif key in [arcade.key.RIGHT, arcade.key.D]:
            self.tecla_direita = False
            self.atualizar_movimento()