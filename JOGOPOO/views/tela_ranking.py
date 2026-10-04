import arcade
from config import LARGURA, ALTURA
from models.pontuacao import Pontuacao


class TelaRanking(arcade.View):

    def __init__(self):
        super().__init__()

        # Fundo
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite("sprites/fundo.jpeg")
        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2
        background.width = LARGURA
        background.height = ALTURA

        self.background_list.append(background)

        # A consulta ao banco é feita UMA ÚNICA VEZ aqui no __init__
        # e guardada em self.melhores. O on_draw só lê essa lista.
        self.melhores = Pontuacao.top10()


    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_RED


    def on_draw(self):

        self.clear()

        self.background_list.draw()

        # Título
        arcade.draw_text(
            "TOP 10 - RANKING",
            LARGURA // 2,
            ALTURA - 100,
            arcade.color.GOLD,
            40,
            anchor_x="center"
        )

        # Banco vazio
        if len(self.melhores) == 0:
            arcade.draw_text(
                "Nenhuma pontuação registrada ainda.\nJogue uma partida!",
                LARGURA // 2,
                ALTURA // 2,
                arcade.color.WHITE,
                24,
                anchor_x="center",
                multiline=True,
                align="center",
                width=700
            )

        else:
            self.desenhar_tabela()

        arcade.draw_text(
            "[M] ou [ESC] - Voltar ao Menu",
            LARGURA // 2,
            50,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )


    def desenhar_tabela(self):

        # Cabeçalho (cada coluna tem um X fixo para ficar alinhada)
        y_cabecalho = ALTURA - 160

        arcade.draw_text("#", 110, y_cabecalho, arcade.color.GOLD, 18, anchor_x="right")
        arcade.draw_text("Jogador", 140, y_cabecalho, arcade.color.GOLD, 18)
        arcade.draw_text("Pontos", 520, y_cabecalho, arcade.color.GOLD, 18, anchor_x="right")
        arcade.draw_text("Tempo", 640, y_cabecalho, arcade.color.GOLD, 18, anchor_x="right")
        arcade.draw_text("Data", 680, y_cabecalho, arcade.color.GOLD, 18)

        # Uma linha por pontuação: o Y depende do índice
        for indice, registro in enumerate(self.melhores):

            y = ALTURA - 205 - indice * 42

            if indice == 0:
                cor = arcade.color.GOLD
            else:
                cor = arcade.color.WHITE

            data = registro.data_hora.strftime("%d/%m/%Y")

            arcade.draw_text(f"{indice + 1}º", 110, y, cor, 20, anchor_x="right")
            arcade.draw_text(registro.nome_jogador, 140, y, cor, 20)
            arcade.draw_text(str(registro.pontos), 520, y, cor, 20, anchor_x="right")
            arcade.draw_text(f"{registro.tempo_partida:.1f}s", 640, y, cor, 20, anchor_x="right")
            arcade.draw_text(data, 680, y, cor, 20)


    def on_key_press(self, key, modifiers):

        if key == arcade.key.M or key == arcade.key.ESCAPE:

            from views.menu_view import MenuView
            self.window.show_view(MenuView())