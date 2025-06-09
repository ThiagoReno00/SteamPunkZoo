# Arquivo: menu.py
import pygame

def tela_de_menu(tela):
    """
    Função para exibir e gerenciar a tela de menu.
    Retorna "iniciar" ou "sair".
    """
    largura, altura = tela.get_size()
    
    # Cores e Fontes
    BRANCO = (255, 255, 255)
    CINZA = (80, 80, 80)
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_botao = pygame.font.Font(None, 50)

    # Botões
    botao_iniciar = pygame.Rect(largura // 2 - 150, altura // 2 - 25, 300, 50)
    botao_sair = pygame.Rect(largura // 2 - 150, altura // 2 + 50, 300, 50)

    # Carregar imagem de fundo do menu
    try:
        # !!! Coloque o nome da imagem de fundo do seu menu aqui !!!
        fundo_menu_img = pygame.image.load('cenario floresta.png').convert()
        # --- MUDANÇA 1: REDIMENSIONANDO O FUNDO ---
        # Garante que a imagem preencha a tela, não importa o tamanho original dela
        fundo_menu_img = pygame.transform.scale(fundo_menu_img, (largura, altura))
    except pygame.error:
        fundo_menu_img = None

    # Loop do Menu
    while True:
        # 1. PROCESSAR EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.collidepoint(evento.pos):
                    return "iniciar"
                if botao_sair.collidepoint(evento.pos):
                    return "sair"

        # 2. ÁREA DE DESENHO
        # --- MUDANÇA 2: LIMPANDO A TELA ---
        # Limpa a tela com preto antes de desenhar, para apagar "fantasmas" de outras telas
        tela.fill((0, 0, 0))

        # Desenha o fundo (agora do tamanho certo)
        if fundo_menu_img:
            tela.blit(fundo_menu_img, (0, 0))
        # Se não houver imagem, o fundo já estará preto por causa do tela.fill()

        # Desenha os outros elementos por cima
        # Título
        texto_titulo = fonte_titulo.render("Batalha Animal", True, BRANCO)
        tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 150))

        # Botão Iniciar
        pygame.draw.rect(tela, CINZA, botao_iniciar)
        texto_iniciar = fonte_botao.render("Iniciar Jogo", True, BRANCO)
        tela.blit(texto_iniciar, (botao_iniciar.x + 50, botao_iniciar.y + 10))

        # Botão Sair
        pygame.draw.rect(tela, CINZA, botao_sair)
        texto_sair = fonte_botao.render("Sair", True, BRANCO)
        tela.blit(texto_sair, (botao_sair.x + 120, botao_sair.y + 10))

        # 3. ATUALIZAR A TELA
        pygame.display.flip()