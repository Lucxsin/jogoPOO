import arcade

from config import (
    LARGURA,
    ALTURA,
    VELOCIDADE_JOGADOR,
    TEMPO_FRAME_ANIMACAO,
)

# Dados da spritesheet (sprites/jogador_sheet.png)
TAMANHO_QUADRO = 200     # cada quadro tem 200x200 px
COLUNAS = 6              # quadros por linha
INDICE_PARADO = 0
INDICES_CAMINHADA = [1, 2, 3, 4]
INDICE_PULO = 5


class Player(arcade.Sprite):

    def __init__(self):
        # Carrega a folha de sprites e fatia em quadros
        folha = arcade.load_spritesheet("sprites/jogador_sheet.png")
        texturas = folha.get_texture_grid(
            size=(TAMANHO_QUADRO, TAMANHO_QUADRO),
            columns=COLUNAS,
            count=COLUNAS * 2,
        )

        # Linha 0 = olhando para a direita | linha 1 = olhando para a esquerda
        self.texturas_direita = texturas[:COLUNAS]
        self.texturas_esquerda = texturas[COLUNAS:]

        super().__init__(self.texturas_direita[INDICE_PARADO], scale=0.5)

        # Controle da animação
        self.virado_para = "direita"
        self.frame_atual = 0
        self.tempo_frame = 0.0

    # ---------- Movimento horizontal (o pulo é tratado na GameView) ----------
    def mover_esquerda(self):
        self.change_x = -VELOCIDADE_JOGADOR
        self.virado_para = "esquerda"

    def mover_direita(self):
        self.change_x = VELOCIDADE_JOGADOR
        self.virado_para = "direita"

    def parar_horizontal(self):
        self.change_x = 0

    # ---------- Máquina de estados da animação ----------
    def update(self, delta_time=1 / 60):
        # Quem move o jogador é o PhysicsEnginePlatformer.
        # Aqui só escolhemos a textura certa.

        # Guarda para qual lado ele está virado
        if self.change_x < 0:
            self.virado_para = "esquerda"
        elif self.change_x > 0:
            self.virado_para = "direita"

        if self.virado_para == "direita":
            texturas = self.texturas_direita
        else:
            texturas = self.texturas_esquerda

        # Prioridade 1: PULO / QUEDA
        if self.change_y != 0:
            self.texture = texturas[INDICE_PULO]
            self.frame_atual = 0
            self.tempo_frame = 0.0

        # Prioridade 2: PARADO (idle)
        elif self.change_x == 0:
            self.texture = texturas[INDICE_PARADO]
            self.frame_atual = 0
            self.tempo_frame = 0.0

        # Prioridade 3: ANDANDO (walk) - troca de quadro a cada 100 ms
        else:
            self.tempo_frame += delta_time

            if self.tempo_frame >= TEMPO_FRAME_ANIMACAO:
                self.tempo_frame -= TEMPO_FRAME_ANIMACAO
                self.frame_atual = (self.frame_atual + 1) % len(INDICES_CAMINHADA)

            self.texture = texturas[INDICES_CAMINHADA[self.frame_atual]]

        # Limites da tela (esquerda, direita e topo)
        if self.left < 0:
            self.left = 0

        if self.right > LARGURA:
            self.right = LARGURA

        if self.top > ALTURA:
            self.top = ALTURA