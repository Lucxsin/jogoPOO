import arcade

from config import TAMANHO_BLOCO


class Bloco(arcade.Sprite):
    """Bloco sólido usado no chão e nas plataformas suspensas."""

    def __init__(self, x, y):
        super().__init__("sprites/bloco.png")

        # Garante que o bloco tenha sempre o tamanho da grade (50x50)
        self.width = TAMANHO_BLOCO
        self.height = TAMANHO_BLOCO

        self.center_x = x
        self.center_y = y