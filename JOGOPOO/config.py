#Janela
LARGURA = 900
ALTURA = 700
TITULO = "Guerra Dentro do Corpo Humano"

#Jogo
VELOCIDADE_JOGADOR = 5
PONTUACAO_MAXIMA = 35

#Física de plataforma
GRAVIDADE = 0.6          # quanto a gravidade puxa o jogador para baixo a cada frame
FORCA_PULO = 15          # velocidade vertical inicial do pulo
TAMANHO_BLOCO = 50       # os blocos são quadrados de 50x50 px

#Animação do jogador
TEMPO_FRAME_ANIMACAO = 0.1   # troca de quadro a cada 100 ms

#Onde o jogador nasce (os inimigos nascem longe daqui)
SPAWN_X = LARGURA // 2
SPAWN_Y = TAMANHO_BLOCO + 60