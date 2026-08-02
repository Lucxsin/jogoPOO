import arcade
from config import LARGURA, ALTURA


class AboutView(arcade.View):

    def __init__(self):
        super().__init__()

        # Fundo
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite("sprites/about.jpeg")

        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2

        background.width = LARGURA
        background.height = ALTURA

        self.background_list.append(background)


        # Avatares
        self.avatar_list = arcade.SpriteList()


        avatar1 = arcade.Sprite("sprites/avatar1.jpeg")
        avatar1.center_x = 300
        avatar1.center_y = 230
        avatar1.width = 180
        avatar1.height = 180

        self.avatar_list.append(avatar1)


        avatar2 = arcade.Sprite("sprites/avatar1.jpeg")
        avatar2.center_x = 600
        avatar2.center_y = 230
        avatar2.width = 180
        avatar2.height = 180

        self.avatar_list.append(avatar2)



    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_RED



    def on_draw(self):

        self.clear()


        # Fundo
        self.background_list.draw()


        # Avatares
        self.avatar_list.draw()



        # Título

        arcade.draw_text(
            "SOBRE O JOGO",
            LARGURA // 2,
            ALTURA - 100,
            arcade.color.GOLD,
            40,
            anchor_x="center"
        )


        # História do jogo

        descricao = (
            "Uma bactéria misteriosa invadiu o organismo.\n"
            "Você é um glóbulo branco de elite chamado Leuco-X,\n"
            "responsável por proteger o corpo e eliminar\n"
            "a infecção antes que ela se espalhe."
        )


        arcade.draw_text(
            descricao,
            LARGURA // 2,
            ALTURA - 150,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            multiline=True,
            align="center",
            width=700
        )


        # Autoria

        arcade.draw_text(
            "Projeto desenvolvido por:",
            LARGURA // 2,
            350,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )


        # Nomes

        arcade.draw_text(
            "Nome Integrante 1",
            300,
            130,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )


        arcade.draw_text(
            "Nome Integrante 2",
            600,
            130,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )


        # Retorno

        arcade.draw_text(
            "[M] ou [ESC] - Voltar ao Menu",
            LARGURA // 2,
            60,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )



    def on_key_press(self, key, modifiers):

        if key == arcade.key.M or key == arcade.key.ESCAPE:

            from views.menu_view import MenuView

            self.window.show_view(MenuView())