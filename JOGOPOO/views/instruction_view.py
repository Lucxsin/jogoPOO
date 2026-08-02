import arcade
from config import LARGURA, ALTURA


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()

        # Fundo da tela de instruções
        self.background_list = arcade.SpriteList()

        background = arcade.Sprite("sprites/fundo.jpeg")

        background.center_x = LARGURA / 2
        background.center_y = ALTURA / 2

        background.width = LARGURA
        background.height = ALTURA

        self.background_list.append(background)


    def on_show_view(self):
        self.window.background_color = arcade.color.DARK_RED


    def on_draw(self):

        self.clear()

        # Desenha o fundo
        self.background_list.draw()


        # Título

        arcade.draw_text(
            "INSTRUÇÕES",
            LARGURA // 2,
            ALTURA - 100,
            arcade.color.GOLD,
            40,
            anchor_x="center"
        )


        texto = (
            "OBJETIVO DO JOGO:\n"
            "Colete todas as vitaminas(+1) e antibióticos(+5)\n"
            "para alcançar a maior pontuação.\n\n"

            "INIMIGOS:\n"
            "As bactérias movem-se pelo cenário, cuidado para não colidir\n"
            "causa perda de 1 ponto.\n"
            "A super bactéria persegue o jogador e causa perda 1 pontoabout\n ao tocar nele.\n\n"

            "CONTROLES:\n"
            "W ou ↑  - Mover para cima\n"
            "S ou ↓  - Mover para baixo\n"
            "A ou ←  - Mover para esquerda\n"
            "D ou →  - Mover para direita\n\n"

            "[M] ou [ESC] - Voltar ao Menu"
        )


        arcade.draw_text(
            texto,
            LARGURA // 2,
            ALTURA -145,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            multiline=True,
            align="center",
            width=700
        )


    def on_key_press(self, key, modifiers):

        if key == arcade.key.M or key == arcade.key.ESCAPE:

            from views.menu_view import MenuView
            self.window.show_view(MenuView())