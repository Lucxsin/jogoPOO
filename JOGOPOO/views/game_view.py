import arcade

# Tamanho da tela
LARGURA = 800
ALTURA = 600

# Velocidade do jogador
VELOCIDADE = 5


class GameView(arcade.View):

    def __init__(self):
        super().__init__()

        # Carrega o cenário
        self.background = arcade.load_texture("sprites/cenario.jpg")

        # Carrega as texturas do jogador
        self.player_baixo = arcade.load_texture("sprites/gb_baixo.png")
        self.player_cima = arcade.load_texture("sprites/gb_atras.png")
        self.player_esquerda = arcade.load_texture("sprites/gb_esquerda.png")
        self.player_direita = arcade.load_texture("sprites/gb_direita.png")

        # Cria o jogador
        self.player = arcade.Sprite()

        self.player.texture = self.player_baixo
        self.player.center_x = 400
        self.player.center_y = 300

    def on_draw(self):

        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            0,
            0,
            LARGURA,
            ALTURA,
            self.background
        )

        self.player.draw()

    def on_update(self, delta_time):

        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        # Limites da tela

        if self.player.left < 0:
            self.player.left = 0

        if self.player.right > LARGURA:
            self.player.right = LARGURA

        if self.player.bottom < 0:
            self.player.bottom = 0

        if self.player.top > ALTURA:
            self.player.top = ALTURA

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.player.change_x = -VELOCIDADE
            self.player.texture = self.player_esquerda

        elif key == arcade.key.RIGHT:
            self.player.change_x = VELOCIDADE
            self.player.texture = self.player_direita

        elif key == arcade.key.UP:
            self.player.change_y = VELOCIDADE
            self.player.texture = self.player_cima

        elif key == arcade.key.DOWN:
            self.player.change_y = -VELOCIDADE
            self.player.texture = self.player_baixo

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0