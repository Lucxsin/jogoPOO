import arcade
from config import LARGURA, ALTURA


class MenuView(arcade.View):

    def __init__(self):
        super().__init__()

         # Fundo do menu
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite("sprites/menu.jpeg")

        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2

        background.width = LARGURA
        background.height = ALTURA

        self.background_list.append(background)

    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_RED

    def on_draw(self):
        self.clear()

        self.background_list.draw()


        arcade.draw_text(
            "[J] Jogar",
            450,
            400,
            arcade.color.WHITE,
            25,
            anchor_x="center"
        )

        arcade.draw_text(
            "[I] Instruções",
            450,
            350,
            arcade.color.WHITE,
            25,
            anchor_x="center"
        )

        arcade.draw_text(
            "[S] Sobre",
            450,
            300,
            arcade.color.WHITE,
            25,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Sair",
            450,
            250,
            arcade.color.WHITE,
            25,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        # Jogar
        if key == arcade.key.J:
            from views.game_view import GameView
            self.window.show_view(GameView())

        # Instruções
        elif key == arcade.key.I:
            from views.instruction_view import InstructionView
            self.window.show_view(InstructionView())

        # Sobre
        elif key == arcade.key.S:
            from views.about_view import AboutView
            self.window.show_view(AboutView())

        # Sair
        elif key == arcade.key.ESCAPE:
            arcade.exit()