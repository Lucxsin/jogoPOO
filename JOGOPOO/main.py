import arcade

from views.menu_view import MenuView

# Configurações da janela
LARGURA = 800
ALTURA = 600
TITULO = "Meu Jogo"


def main():
    # Cria a janela
    window = arcade.Window(LARGURA, ALTURA, TITULO)

    # Abre o menu
    menu = MenuView()
    window.show_view(menu)

    # Inicia o jogo
    arcade.run()


if __name__ == "__main__":
    main()