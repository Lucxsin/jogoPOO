import arcade

from config import LARGURA, ALTURA, TITULO  
from views.menu_view import MenuView



def main():
    # Cria a janela
    window = arcade.Window(
    LARGURA,
    ALTURA,
    TITULO,
    
    )

    # Abre o menu
    menu = MenuView()
    window.show_view(menu)

    # Inicia o jogo
    arcade.run()


if __name__ == "__main__":
    main()