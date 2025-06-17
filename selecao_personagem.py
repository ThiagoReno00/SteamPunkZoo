# Arquivo: selecao_personagem.py
import pygame
from personagens_status import PERSONAGENS_BASE

def tela_selecao_personagem(tela_logica, tela_real):
    largura, altura = tela_logica.get_size()
    LARGURA_REAL, ALTURA_REAL = tela_real.get_size()
    BRANCO = (255, 255, 255)
    CINZA = (80, 80, 80)
    PRETO = (0, 0, 0)
    fonte_titulo = pygame.font.Font(None, 74)
    # --- MUDANÇA: A FONTE PARA O NOME FOI REMOVIDA ---
    # fonte_nome = pygame.font.Font(None, 40) # Não é mais necessária

    try:
        fundo_img = pygame.image.load('fundo_selecao.png').convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
    except pygame.error as e:
        print(f"Erro ao carregar imagem de fundo da seleção: {e}")
        fundo_img = None

    personagens_jogaveis = ["Urso", "Raposa", "Ganso", "Pinguim", "Iguana", "Tigre"]

    itens_selecao = []
    num_personagens = len(personagens_jogaveis)
    fatia_largura = largura / (num_personagens + 1)
    
    for i, nome_chave in enumerate(personagens_jogaveis):
        try:
            p_info = PERSONAGENS_BASE[nome_chave]
            icone = pygame.image.load(p_info["icone_path"]).convert_alpha()
            icone = pygame.transform.scale(icone, (150, 150))
            pos_x_centro = int((i + 1) * fatia_largura)
            rect = icone.get_rect(center=(pos_x_centro, altura // 2))
            # A gente ainda precisa dos dados, mas não mais do 'nome_display'
            itens_selecao.append({"chave_personagem": nome_chave, "icone": icone, "rect": rect})
        except Exception as e:
            print(f"Erro ao carregar dados do personagem '{nome_chave}': {e}")

    clock = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return None
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_real, mouse_y_real = evento.pos
                escala_x = largura / LARGURA_REAL
                escala_y = altura / ALTURA_REAL
                pos_mouse_logico = (mouse_x_real * escala_x, mouse_y_real * escala_y)
                for item in itens_selecao:
                    if item["rect"].collidepoint(pos_mouse_logico):
                        return item["chave_personagem"]

        if fundo_img:
            tela_logica.blit(fundo_img, (0, 0))
        else:
            tela_logica.fill(PRETO)

        texto_titulo = fonte_titulo.render("Escolha seu Lutador", True, BRANCO)
        tela_logica.blit(texto_titulo, (largura // 2 - texto_titulo.get_width() // 2, 80))

        # Desenha cada personagem
        for item in itens_selecao:
            tela_logica.blit(item["icone"], item["rect"])
            pygame.draw.rect(tela_logica, CINZA, item["rect"], 3)
            
            # --- MUDANÇA: AS LINHAS QUE DESENHAVAM O NOME FORAM REMOVIDAS DAQUI ---
            # texto_nome = fonte_nome.render(item["nome_display"], True, BRANCO)
            # tela_logica.blit(texto_nome, ...)

        tela_projetada = pygame.transform.scale(tela_logica, (LARGURA_REAL, ALTURA_REAL))
        tela_real.blit(tela_projetada, (0, 0))
        pygame.display.flip()
        clock.tick(60)
