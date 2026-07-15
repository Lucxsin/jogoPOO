import arcade


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_BLUE

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "MEU JOGO",
            400,
            450,
            arcade.color.WHITE,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "[J] Jogar",
            400,
            300,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            400,
            260,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre",
            400,
            220,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            400,
            180,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )