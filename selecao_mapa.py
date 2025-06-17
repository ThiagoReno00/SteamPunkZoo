# Arquivo: selecao_mapa.py
import pygame

def tela_selecao_mapa(tela_logica, tela_real):
    largura, altura = tela_logica.get_size()
    LARGURA_REAL, ALTURA_REAL = tela_real.get_size()
    BRANCO = (255, 255, 255); CINZA = (80, 80, 80)
    fonte_titulo = pygame.font.Font(None, 74); fonte_nome = pygame.font.Font(None, 30)

    try:
        fundo_img = pygame.image.load('fundo_mapa.png').convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
    except pygame.error as e:
        print(f"Erro ao carregar fundo da seleção de mapa: {e}"); fundo_img = None

    mapas = [
        {"nome": "Floresta Verde", "thumb_path": "cenario_floresta.jpg", "bg_path": "cenario_floresta.jpg"},
        {"nome": "Montanhas Nevadas", "thumb_path": "cenario_gelo.jpg", "bg_path": "cenario_gelo.jpg"},
        {"nome": "Deserto", "thumb_path": "cenario_deserto.jpg", "bg_path": "cenario_deserto.jpg"}
    ]

    itens_selecao = []
    num_mapas = len(mapas)
    fatia_largura = largura / (num_mapas + 1)
    
    for i, m_info in enumerate(mapas):
        try:
            thumb = pygame.image.load(m_info["thumb_path"]).convert()
            thumb = pygame.transform.scale(thumb, (200, 150))
            pos_x_centro = int((i + 1) * fatia_largura)
            rect = thumb.get_rect(center=(pos_x_centro, altura // 2))
            itens_selecao.append({"dados": m_info, "thumb": thumb, "rect": rect})
        except pygame.error as e:
            print(f"Erro ao carregar miniatura do mapa {m_info['nome']}: {e}")

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_real, mouse_y_real = evento.pos
                escala_x = largura / LARGURA_REAL
                escala_y = altura / ALTURA_REAL
                pos_mouse_logico = (mouse_x_real * escala_x, mouse_y_real * escala_y)
                for item in itens_selecao:
                    if item["rect"].collidepoint(pos_mouse_logico): return item["dados"]["bg_path"]

        if fundo_img: tela_logica.blit(fundo_img, (0, 0))
        else: tela_logica.fill((0, 0, 0))

        texto_titulo = fonte_titulo.render("Escolha o Cenário", True, BRANCO)
        tela_logica.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 80))

        for item in itens_selecao:
            tela_logica.blit(item["thumb"], item["rect"])
            pygame.draw.rect(tela_logica, CINZA, item["rect"], 3)
            texto_nome = fonte_nome.render(item["dados"]["nome"], True, BRANCO)
            tela_logica.blit(texto_nome, (item["rect"].centerx - texto_nome.get_width() // 2, item["rect"].bottom + 10))

        tela_projetada = pygame.transform.scale(tela_logica, (LARGURA_REAL, ALTURA_REAL))
        tela_real.blit(tela_projetada, (0, 0))
        pygame.display.flip()
        clock.tick(60)
