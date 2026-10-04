import arcade
from config import LARGURA, ALTURA, PONTUACAO_MAXIMA
from models.pontuacao import Pontuacao

TAMANHO_MAXIMO_NOME = 15


class GameOverView(arcade.View):

    def __init__(self, pontuacao, tempo_total):
        super().__init__()

        self.pontuacao = pontuacao
        self.tempo_total = tempo_total

        # Primeiro digita o nome, depois de salvar mostra os atalhos
        self.nome = ""
        self.salvo = False
        self.erro_ao_salvar = False


    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK


    def on_draw(self):

        self.clear()

        if self.pontuacao == PONTUACAO_MAXIMA:

            titulo = "VITÓRIA PERFEITA!"
            cor = arcade.color.GOLD

            mensagem = (
                "PARABÉNS!\n"
                "Você escapou de todos os inimigos\n"
                "sem sofrer nenhum dano!"
            )

        else:

            titulo = "FIM DE JOGO!"
            cor = arcade.color.RED

            mensagem = (
                "Parabéns por concluir o jogo!\n"
                "Continue tentando melhorar sua pontuação."
            )

        arcade.draw_text(
            titulo,
            LARGURA // 2,
            ALTURA - 150,
            cor,
            45,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Pontuação final: {self.pontuacao}",
            LARGURA // 2,
            ALTURA - 250,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        minutos = int(self.tempo_total) // 60
        segundos = int(self.tempo_total) % 60

        arcade.draw_text(
            f"Tempo total: {minutos:02}:{segundos:02}",
            LARGURA // 2,
            ALTURA - 300,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            mensagem,
            LARGURA // 2,
            ALTURA // 2,
            arcade.color.GREEN,
            22,
            anchor_x="center",
            multiline=True,
            align="center",
            width=600
        )

        if not self.salvo:
            self.desenhar_campo_nome()
        else:
            self.desenhar_atalhos()


    def desenhar_campo_nome(self):
        # Campo de digitação do nome do jogador

        arcade.draw_text(
            "Digite seu nome para o ranking:",
            LARGURA // 2,
            215,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            self.nome + "_",
            LARGURA // 2,
            170,
            arcade.color.GOLD,
            28,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ENTER] Salvar     [ESC] Pular",
            LARGURA // 2,
            100,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )


    def desenhar_atalhos(self):
        # Mostrado depois que a pontuação foi salva

        if self.erro_ao_salvar:
            arcade.draw_text(
                "Não foi possível salvar a pontuação.",
                LARGURA // 2,
                200,
                arcade.color.RED,
                20,
                anchor_x="center"
            )
        else:
            arcade.draw_text(
                "Pontuação salva no ranking!",
                LARGURA // 2,
                200,
                arcade.color.GOLD,
                22,
                anchor_x="center"
            )

        arcade.draw_text(
            "[R] Ver Ranking     [M] Menu Principal",
            LARGURA // 2,
            150,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair do Jogo",
            LARGURA // 2,
            100,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )


    def salvar_pontuacao(self):
        nome = self.nome.strip() or "Anônimo"

        registro = Pontuacao.registrar(nome, self.pontuacao, self.tempo_total)

        if registro is None:
            self.erro_ao_salvar = True
        else:
            print(registro)     # usa o __str__ do modelo (ajuda na depuração)

        self.salvo = True


    def on_text(self, text):
        # Recebe os caracteres digitados (letras, números, espaço...)
        if self.salvo:
            return

        if text.isprintable() and len(self.nome) < TAMANHO_MAXIMO_NOME:
            self.nome += text


    def on_key_press(self, key, modifiers):

        # Etapa 1: digitando o nome
        if not self.salvo:

            if key == arcade.key.ENTER or key == arcade.key.NUM_ENTER:
                self.salvar_pontuacao()

            elif key == arcade.key.BACKSPACE:
                self.nome = self.nome[:-1]

            elif key == arcade.key.ESCAPE:
                from views.menu_view import MenuView
                self.window.show_view(MenuView())

            return

        # Etapa 2: pontuação já salva
        if key == arcade.key.M:

            from views.menu_view import MenuView
            self.window.show_view(MenuView())

        elif key == arcade.key.R:

            from views.tela_ranking import TelaRanking
            self.window.show_view(TelaRanking())

        elif key == arcade.key.ESCAPE:

            arcade.close_window()