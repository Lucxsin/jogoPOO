import arcade


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_GREEN

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "INSTRUÇÕES",
            400,
            500,
            arcade.color.WHITE,
            35,
            anchor_x="center"
        )

        arcade.draw_text(
            "• Use as setas para mover o personagem\n"
            "• Colete moedas para ganhar pontos\n"
            "• Desvie dos inimigos\n\n"
            "Pressione ESC para voltar",
            400,
            320,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            multiline=True,
            width=600
        )

    def on_key_press(self, key, modifiers):
        print("Tecla pressionada:", key)

        if key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())