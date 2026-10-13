import arcade

import random

from config import (
    LARGURA,
    ALTURA,
    GRAVIDADE,
    FORCA_PULO,
    TAMANHO_BLOCO,
    SPAWN_X,
    TEMPO_INVENCIVEL,
    TEMPO_FLASH,
    TEMPO_TREMOR,
    INTENSIDADE_TREMOR
)

from classes.jogador import Player
from classes.bloco import Bloco
from classes.vitamina import Vitamina
from classes.bacteria import Bacteria
from classes.antibiotico import Antibiotico
from classes.super_bacteria import SuperBacteria
from views.game_over_view import GameOverView
from classes.explosao import Explosao


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

        # Temporizadores dos efeitos de colisão
        self.tempo_invencivel = 0.0
        self.tempo_flash = 0.0
        self.tempo_tremor = 0.0

        # Câmera usada para o tremor
        self.camera = arcade.Camera2D()

        # Lista de efeitos visuais
        self.sprite_efeitos = arcade.SpriteList()

        # Carrega a spritesheet da explosão
        folha_explosao = arcade.load_spritesheet(
            "sprites/explosao_768x128-.png"
        )

        # Separa a imagem em 6 quadros de 128 x 128 pixels
        self.quadros_explosao = folha_explosao.get_texture_grid(
            size=(128, 128),
            columns=6,
            count=6
        )

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

         # Mundo do jogo: a câmera permite o tremor
        self.camera.use()

        self.background_list.draw()
        self.bloco_list.draw()
        self.vitamina_list.draw()
        self.antibiotico_list.draw()
        self.bacteria_list.draw()
        self.super_bacteria_list.draw()
        self.player_list.draw()
        self.sprite_efeitos.draw()

        # Câmera fixa: flash e HUD não tremem
        self.window.default_camera.use()

        # Flash vermelho que desaparece suavemente
        if self.tempo_flash > 0:
            alpha = int(
                120 * self.tempo_flash / TEMPO_FLASH
            )

            arcade.draw_rect_filled(
                arcade.XYWH(
                LARGURA / 2,
                ALTURA / 2,
                LARGURA,
                ALTURA
                ),
                (255, 0, 0, alpha)
            )

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

    def ativar_efeitos_colisao(self, inimigo, escala = 0.7):
          # Ponto médio entre o jogador e o inimigo
            x = (self.player.center_x + inimigo.center_x) / 2
            y = (self.player.center_y + inimigo.center_y) / 2

         # Explosão
            explosao = Explosao(
                x=x,
                y=y,
                quadros=self.quadros_explosao,
                scale=escala
            )
            self.sprite_efeitos.append(explosao)

             # Ativa os três efeitos
            self.tempo_invencivel = TEMPO_INVENCIVEL
            self.tempo_flash = TEMPO_FLASH
            self.tempo_tremor = TEMPO_TREMOR
        

    def on_update(self, delta_time):
        # Atualiza o cronômetro
        self.tempo_jogo += delta_time

        # Atualiza os efeitos
        self.tempo_invencivel = max(
            0.0, self.tempo_invencivel - delta_time
        )
        self.tempo_flash = max(
            0.0, self.tempo_flash - delta_time
        )
        self.tempo_tremor = max(
            0.0, self.tempo_tremor - delta_time
        )

        # Faz o aviso desaparecer depois de 0,5 segundo
        if self.alerta_tempo > 0:
            self.alerta_tempo -= delta_time

        # Tremor: diminui a intensidade até a tela voltar ao centro
        if self.tempo_tremor > 0:
            forca = (
                INTENSIDADE_TREMOR
                * self.tempo_tremor
                / TEMPO_TREMOR
            )

            self.camera.position = (
                LARGURA / 2 + random.uniform(-forca, forca),
                ALTURA / 2 + random.uniform(-forca, forca),
            )
        else:
            self.camera.position = (
                LARGURA / 2,
                ALTURA / 2
            )

        # Física primeiro (move o jogador), depois a animação
        self.physics_engine.update()
        self.player.update(delta_time)

        self.bacteria_list.update()
        self.antibiotico_list.update()
        self.super_bacteria_list.update()
        self.sprite_efeitos.update(delta_time)


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

        
       
        # Colisão com bactérias
        bacterias = arcade.check_for_collision_with_list(
            self.player,
            self.bacteria_list
        )

        if len(bacterias) > 0:
            # Aplica o dano apenas no início da colisão
            if not self.colidindo_bacteria:
                self.pontos -= 1
                self.alerta_tempo = 0.5
                self.colidindo_bacteria = True
                self.sofreu_dano = True

                # Cria a explosão no ponto da colisão
                bacteria = bacterias[0]
                self.ativar_efeitos_colisao(bacteria, escala=0.7)

                explosao = Explosao(
                    x=(self.player.center_x + bacteria.center_x) / 2,
                    y=(self.player.center_y + bacteria.center_y) / 2,
                    quadros=self.quadros_explosao,
                    scale=0.7
                )

                self.sprite_efeitos.append(explosao)

        else:
            # Libera um novo dano quando o jogador se afasta
            self.colidindo_bacteria = False



        
        # Colisão com a super bactéria
        super_bacterias = arcade.check_for_collision_with_list(
            self.player,
            self.super_bacteria_list
        )

        if len(super_bacterias) > 0:
            if not self.colidindo_super:
                self.pontos -= 1
                self.alerta_tempo = 0.5
                self.colidindo_super = True
                self.sofreu_dano = True

                # Cria a explosão no ponto da colisão
                inimigo = super_bacterias[0]
                self.ativar_efeitos_colisao(inimigo, escala=1.0)
                explosao = Explosao(
                    x=(self.player.center_x + inimigo.center_x) / 2,
                    y=(self.player.center_y + inimigo.center_y) / 2,
                    quadros=self.quadros_explosao,
                    scale=1.0
                )

                self.sprite_efeitos.append(explosao)

                # Afasta a super bactéria após a colisão
                for inimigo in super_bacterias:
                    inimigo.teleportar()

        else:
            self.colidindo_super = False

        # Pisca enquanto estiver invencível
        if self.tempo_invencivel > 0:
            if int(self.tempo_invencivel * 10) % 2 == 0:
                self.player.alpha = 80
            else:
                self.player.alpha = 255
        else:
            self.player.alpha = 255
   


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