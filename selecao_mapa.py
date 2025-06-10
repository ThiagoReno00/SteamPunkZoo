# Arquivo: selecao_mapa.py
import pygame

def tela_selecao_mapa(tela):
    largura, altura = tela.get_size()
    BRANCO = (255, 255, 255)
    CINZA = (80, 80, 80)
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_nome = pygame.font.Font(None, 30)

    # --- MUDANÇA 1: CARREGAR A IMAGEM DE FUNDO ---
    try:
        fundo_img = pygame.image.load('fundo_mapa.png').convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo da seleção de mapa: {e}")
        fundo_img = None

    # --- DEFINA SEUS MAPAS AQUI ---
    mapas = [
        {
            "nome": "Floresta Verde",
            "thumb_path": "cenario_floresta.jpg",
            "bg_path": "cenario_floresta.jpg"
        },
        {
            "nome": "Montanhas Nevadas",
            "thumb_path": "cenario_gelo.jpg",
            "bg_path": "cenario_gelo.jpg"
        },
        {
            "nome": "Deserto",
            "thumb_path": "cenario_deserto.jpg",
            "bg_path": "cenario_deserto.jpg"
        }
    ]

    itens_selecao = []
    pos_x_inicial = 250
    espacamento = 300
    for i, m_info in enumerate(mapas):
        try:
            thumb = pygame.image.load(m_info["thumb_path"]).convert()
            thumb = pygame.transform.scale(thumb, (200, 150))
            rect = thumb.get_rect(center=(pos_x_inicial + i * espacamento, altura // 2))
            itens_selecao.append({"dados": m_info, "thumb": thumb, "rect": rect})
        except pygame.error as e:
            print(f"Erro ao carregar miniatura do mapa {m_info['nome']}: {e}")

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for item in itens_selecao:
                    if item["rect"].collidepoint(evento.pos):
                        return item["dados"]["bg_path"]

        # --- MUDANÇA 2: DESENHAR A IMAGEM DE FUNDO ---
        if fundo_img:
            tela.blit(fundo_img, (0, 0))
        else:
            tela.fill((0, 0, 0))

        texto_titulo = fonte_titulo.render("Escolha o Cenário", True, BRANCO)
        tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 80))

        for item in itens_selecao:
            tela.blit(item["thumb"], item["rect"])
            pygame.draw.rect(tela, CINZA, item["rect"], 3)
            texto_nome = fonte_nome.render(item["dados"]["nome"], True, BRANCO)
            tela.blit(texto_nome, (item["rect"].centerx - texto_nome.get_width() // 2, item["rect"].bottom + 10))

        pygame.display.flip()
        clock.tick(60)
