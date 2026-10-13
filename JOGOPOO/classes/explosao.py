
import arcade


class Explosao(arcade.Sprite):

    def __init__(self, x, y, quadros, scale=1.0):
        # Começa pelo primeiro quadro da animação
        super().__init__(quadros[0], scale=scale)

        # Posição em que a explosão aparecerá
        self.center_x = x
        self.center_y = y

        # Quadros da spritesheet
        self.quadros = quadros
        self.quadro_atual = 0

        # Controle do tempo da animação
        self.tempo_animacao = 0.0

    def update(self, delta_time=1 / 60):
        self.tempo_animacao += delta_time

        # Troca de quadro a cada 0,06 segundo
        if self.tempo_animacao >= 0.06:
            self.tempo_animacao -= 0.06
            self.quadro_atual += 1

            # Quando acabar a animação, remove a explosão
            if self.quadro_atual >= len(self.quadros):
                self.remove_from_sprite_lists()
                return

            # Mostra o próximo quadro
            self.texture = self.quadros[self.quadro_atual]
