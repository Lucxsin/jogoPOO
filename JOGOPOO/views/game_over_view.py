import arcade
from config import LARGURA, ALTURA, PONTUACAO_MAXIMA


class GameOverView(arcade.View):

    def __init__(self, pontuacao, tempo_total):
        super().__init__()

        self.pontuacao = pontuacao
        self.tempo_total = tempo_total


    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK


    def on_draw(self):

        self.clear()


        # Verifica pontuação máxima

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


        # Título

        arcade.draw_text(
            titulo,
            LARGURA // 2,
            ALTURA - 150,
            cor,
            45,
            anchor_x="center"
        )


        # Pontuação

        arcade.draw_text(
            f"Pontuação final: {self.pontuacao}",
            LARGURA // 2,
            ALTURA - 250,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )


        # Tempo

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


        # Mensagem final

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


        # Comandos

        arcade.draw_text(
            "[M] Voltar ao Menu Principal",
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


    def on_key_press(self, key, modifiers):

        if key == arcade.key.M:

            from views.menu_view import MenuView
            self.window.show_view(MenuView())


        elif key == arcade.key.ESCAPE:

            arcade.close_window()