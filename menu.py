# Arquivo: menu.py
import pygame

def tela_de_menu(tela):
    largura, altura = tela.get_size()
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_TRANSLUCIDO = (80, 80, 80, 180) 
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_botao = pygame.font.Font(None, 50)
    
    botao_iniciar_rect = pygame.Rect(largura // 2 - 150, altura // 2 - 25, 300, 50)
    botao_sair_rect = pygame.Rect(largura // 2 - 150, altura // 2 + 50, 300, 50)
    raio_borda = 15

    try:
        fundo_menu_img = pygame.image.load('fundo_menu.png').convert()
        fundo_menu_img = pygame.transform.scale(fundo_menu_img, (largura, altura))
    except pygame.error:
        fundo_menu_img = None

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar_rect.collidepoint(evento.pos):
                    return "iniciar"
                if botao_sair_rect.collidepoint(evento.pos):
                    return "sair"

        tela.fill(PRETO)
        if fundo_menu_img:
            tela.blit(fundo_menu_img, (0, 0))

        texto_titulo = fonte_titulo.render("SteamPunk Zoo", True, BRANCO)
        texto_contorno = fonte_titulo.render("SteamPunk Zoo", True, PRETO)
        deslocamento_sombra = 2
        tela.blit(texto_contorno, (largura // 2 - texto_titulo.get_width() // 2 - deslocamento_sombra, 150))
        tela.blit(texto_contorno, (largura // 2 - texto_titulo.get_width() // 2 + deslocamento_sombra, 150))
        tela.blit(texto_contorno, (largura // 2 - texto_titulo.get_width() // 2, 150 - deslocamento_sombra))
        tela.blit(texto_contorno, (largura // 2 - texto_titulo.get_width() // 2, 150 + deslocamento_sombra))
        tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 150))

        superficie_botao_iniciar = pygame.Surface(botao_iniciar_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(superficie_botao_iniciar, CINZA_TRANSLUCIDO, superficie_botao_iniciar.get_rect(), border_radius=raio_borda)
        tela.blit(superficie_botao_iniciar, botao_iniciar_rect.topleft)
        texto_iniciar = fonte_botao.render("Iniciar Jogo", True, BRANCO)
        tela.blit(texto_iniciar, (botao_iniciar_rect.centerx - texto_iniciar.get_width() // 2, botao_iniciar_rect.centery - texto_iniciar.get_height() // 2))

        superficie_botao_sair = pygame.Surface(botao_sair_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(superficie_botao_sair, CINZA_TRANSLUCIDO, superficie_botao_sair.get_rect(), border_radius=raio_borda)
        tela.blit(superficie_botao_sair, botao_sair_rect.topleft)
        texto_sair = fonte_botao.render("Sair", True, BRANCO)
        tela.blit(texto_sair, (botao_sair_rect.centerx - texto_sair.get_width() // 2, botao_sair_rect.centery - texto_sair.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)
