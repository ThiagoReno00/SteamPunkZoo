# Arquivo: selecao_personagem.py
import pygame

def tela_selecao_personagem(tela):
    largura, altura = tela.get_size()
    BRANCO = (255, 255, 255)
    CINZA = (80, 80, 80)
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_nome = pygame.font.Font(None, 40)

    # --- MUDANÇA 1: CARREGAR A IMAGEM DE FUNDO ---
    try:
        # !!! Coloque o nome da sua imagem de fundo aqui !!!
        fundo_img = pygame.image.load('fundo_selecao.png').convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo da seleção: {e}")
        fundo_img = None # Se der erro, o fundo fica preto

    # --- DEFINA SEUS PERSONAGENS AQUI ---
    personagens = [
        {
            "nome": "Urso",
            "icone_path": "icone_urso.png",
            "sprite_path": "urso.png",
            "hp": 120, "ataque_n": 10, "ataque_c": 25
        },
        {
            "nome": "Raposa",
            "icone_path": "raposa.png",
            "sprite_path": "raposa.png",
            "hp": 80, "ataque_n": 15, "ataque_c": 30
        }
    ]

    # Carrega os ícones dos personagens
    itens_selecao = []
    pos_x_inicial = 250
    espacamento = 300
    for i, p_info in enumerate(personagens):
        try:
            icone = pygame.image.load(p_info["icone_path"]).convert_alpha()
            icone = pygame.transform.scale(icone, (200, 200))
            rect = icone.get_rect(center=(pos_x_inicial + i * espacamento, altura // 2))
            itens_selecao.append({"dados": p_info, "icone": icone, "rect": rect})
        except pygame.error as e:
            print(f"Erro ao carregar icone do personagem {p_info['nome']}: {e}")

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for item in itens_selecao:
                    if item["rect"].collidepoint(evento.pos):
                        return item["dados"]

        # --- MUDANÇA 2: DESENHAR A IMAGEM DE FUNDO ---
        # Em vez de preencher com preto, desenhamos a nossa imagem
        if fundo_img:
            tela.blit(fundo_img, (0, 0))
        else:
            tela.fill((0, 0, 0)) # Se a imagem não carregou, o fundo fica preto

        # Desenha o título
        texto_titulo = fonte_titulo.render("Escolha seu Lutador", True, BRANCO)
        tela.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 80))

        # Desenha cada personagem
        for item in itens_selecao:
            tela.blit(item["icone"], item["rect"])
            pygame.draw.rect(tela, CINZA, item["rect"], 3)
            texto_nome = fonte_nome.render(item["dados"]["nome"], True, BRANCO)
            tela.blit(texto_nome, (item["rect"].centerx - texto_nome.get_width() // 2, item["rect"].bottom + 10))

        pygame.display.flip()
        clock.tick(60)