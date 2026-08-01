import arcade


class GameOverView(arcade.View):

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "GAME OVER",
            400,
            340,
            arcade.color.RED,
            45,
            anchor_x="center"
        )

        arcade.draw_text(
            "O vírus venceu!",
            400,
            280,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ENTER] Jogar novamente",
            400,
            180,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            "[ESC] Voltar ao menu",
            400,
            140,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.ENTER:
            from views.game_view import GameView
            self.window.show_view(GameView())

        elif key == arcade.key.ESCAPE:
            from views.menu_view import MenuView
            self.window.show_view(MenuView())