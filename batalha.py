# Arquivo: batalha.py
import pygame
import random

# (As funções auxiliares 'desenhar_barra_hp' e 'desenhar_texto_quebra_linha' continuam aqui, sem alterações)
def desenhar_barra_hp(tela, x, y, hp_atual, hp_maximo):
    if hp_atual < 0:
        hp_atual = 0
    LARGURA_BARRA = 200 # Aumentei um pouco o tamanho da barra de volta
    ALTURA_BARRA = 20
    COR_FUNDO = (100, 0, 0)
    COR_FRENTE = (0, 200, 0)
    porcentagem_hp = hp_atual / hp_maximo
    largura_hp_atual = LARGURA_BARRA * porcentagem_hp
    retangulo_fundo = pygame.Rect(x, y, LARGURA_BARRA, ALTURA_BARRA)
    retangulo_frente = pygame.Rect(x, y, largura_hp_atual, ALTURA_BARRA)
    pygame.draw.rect(tela, COR_FUNDO, retangulo_fundo)
    pygame.draw.rect(tela, COR_FRENTE, retangulo_frente)
    pygame.draw.rect(tela, (255,255,255), retangulo_fundo, 2)

def desenhar_texto_quebra_linha(tela, texto, rect, fonte, cor):
    CINZA_MINIMALISTA = (80, 80, 80)
    # Cria uma superfície separada para a caixa de texto com transparência
    superficie_caixa_msg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    superficie_caixa_msg.fill((0, 0, 0, 150)) # Fundo preto translúcido
    tela.blit(superficie_caixa_msg, rect.topleft)

    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    margem = 30
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        tamanho_teste = fonte.size(teste_linha)
        if tamanho_teste[0] < rect.width - margem:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)

    pos_y = rect.y + 15
    for linha in linhas:
        texto_renderizado = fonte.render(linha, True, cor)
        tela.blit(texto_renderizado, (rect.x + 15, pos_y))
        pos_y += fonte.get_height()

# --- MUDANÇA 1: A FUNÇÃO AGORA RECEBE PARÂMETROS ---
def tela_de_batalha(tela, dados_jogador_escolhido, caminho_mapa_fundo):
    largura, altura = tela.get_size()
    BRANCO = (255, 255, 255)
    CINZA_MINIMALISTA = (80, 80, 80)
    
    try:
        # --- MUDANÇA 2: CARREGAMENTO DINÂMICO DE ARQUIVOS ---
        fundo_img = pygame.image.load(caminho_mapa_fundo).convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
        
        jogador_img_original = pygame.image.load(dados_jogador_escolhido["sprite_path"]).convert_alpha()
        
        # O oponente continua fixo por enquanto, mas poderia ser aleatório ou selecionado também
        oponente_img_original = pygame.image.load('raposa.png').convert_alpha() 
    except pygame.error as e:
        print(f"Erro ao carregar imagem na batalha: {e}")
        return "sair"

    TAMANHO_ANIMAL = (250, 250)
    jogador_img = pygame.transform.scale(jogador_img_original, TAMANHO_ANIMAL)
    oponente_img = pygame.transform.scale(oponente_img_original, TAMANHO_ANIMAL)

    margem_chao = 40
    pos_y_animais = altura - TAMANHO_ANIMAL[1] - margem_chao
    margem_lateral = 100
    pos_x_jogador = margem_lateral
    pos_x_oponente = largura - TAMANHO_ANIMAL[0] - margem_lateral
    
    # --- MUDANÇA 3: DADOS DO JOGADOR VÊM DOS PARÂMETROS ---
    jogador = {
        "nome": dados_jogador_escolhido["nome"], 
        "hp_max": dados_jogador_escolhido["hp"], 
        "hp_atual": dados_jogador_escolhido["hp"],
        "ataque_normal": dados_jogador_escolhido["ataque_n"], 
        "ataque_critico": dados_jogador_escolhido["ataque_c"], 
        "pos": (pos_x_jogador, pos_y_animais)
    }
    # Dados do oponente continuam fixos
    oponente = { 
        "nome": "Raposa", "hp_max": 100, "hp_atual": 100, 
        "ataque_normal": 8, "ataque_critico": 20, "pos": (pos_x_oponente, pos_y_animais) 
    }
    
    fonte = pygame.font.Font(None, 36)
    fonte_pequena = pygame.font.Font(None, 22)
    mensagem_batalha = "A batalha começa!"

    altura_botao = 40
    largura_botao = 160
    margem_botoes = 20
    y_botoes = altura - altura_botao - margem_botoes
    x_botao_normal = margem_botoes
    x_botao_critico = margem_botoes + largura_botao + margem_botoes
    botao_normal_rect = pygame.Rect(x_botao_normal, y_botoes, largura_botao, altura_botao)
    botao_critico_rect = pygame.Rect(x_botao_critico, y_botoes, largura_botao, altura_botao)
    botao_voltar_rect = pygame.Rect(largura // 2 - 150, altura - 70, 300, 50)

    largura_caixa_msg = 300
    altura_caixa_msg = 100
    margem_caixa = 20
    pos_x_caixa_msg = largura - largura_caixa_msg - margem_caixa
    pos_y_caixa_msg = altura - altura_caixa_msg - margem_caixa
    caixa_mensagem_rect = pygame.Rect(pos_x_caixa_msg, pos_y_caixa_msg, largura_caixa_msg, altura_caixa_msg)

    turno_do_jogador = True
    oponente_esta_pensando = False
    tempo_de_espera = 1500
    tempo_inicio_espera = 0
    jogo_acabou = False
    clock = pygame.time.Clock()

    rodando_batalha = True
    while rodando_batalha:
        # (A lógica de eventos, ataques, etc. continua a mesma)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return "sair"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if turno_do_jogador and not jogo_acabou and not oponente_esta_pensando:
                    acao_realizada = False
                    if botao_normal_rect.collidepoint(evento.pos):
                        if random.random() < 0.9:
                            dano = jogador['ataque_normal']
                            oponente['hp_atual'] -= dano
                            mensagem_batalha = f"{jogador['nome']} acertou e causou {dano} de dano!"
                        else:
                            mensagem_batalha = f"{jogador['nome']} errou o ataque!"
                        acao_realizada = True
                    elif botao_critico_rect.collidepoint(evento.pos):
                        if random.random() < 0.5:
                            dano = jogador['ataque_critico']
                            oponente['hp_atual'] -= dano
                            mensagem_batalha = f"CRÍTICO! {jogador['nome']} causou {dano} de dano!"
                        else:
                            mensagem_batalha = f"{jogador['nome']} tentou um ataque crítico e errou!"
                        acao_realizada = True
                    if acao_realizada:
                        turno_do_jogador = False
                        oponente_esta_pensando = True
                        tempo_inicio_espera = pygame.time.get_ticks()
                if jogo_acabou and botao_voltar_rect.collidepoint(evento.pos):
                    return "voltar_menu"
        if oponente_esta_pensando and not jogo_acabou:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_inicio_espera > tempo_de_espera:
                if random.random() < 0.3:
                    if random.random() < 0.5:
                        dano_ia = oponente['ataque_critico']
                        jogador['hp_atual'] -= dano_ia
                        mensagem_batalha = f"{oponente['nome']} usou um ataque CRÍTICO!"
                    else:
                        mensagem_batalha = f"{oponente['nome']} tentou um ataque crítico e errou!"
                else:
                    if random.random() < 0.9:
                        dano_ia = oponente['ataque_normal']
                        jogador['hp_atual'] -= dano_ia
                        mensagem_batalha = f"{oponente['nome']} atacou e causou {dano_ia} de dano!"
                    else:
                        mensagem_batalha = f"{oponente['nome']} errou o ataque!"
                oponente_esta_pensando = False
                turno_do_jogador = True
        if oponente['hp_atual'] <= 0 and not jogo_acabou:
            oponente['hp_atual'] = 0; mensagem_batalha = "VOCÊ VENCEU!"; jogo_acabou = True
        if jogador['hp_atual'] <= 0 and not jogo_acabou:
            jogador['hp_atual'] = 0; mensagem_batalha = "VOCÊ PERDEU!"; jogo_acabou = True

        # --- ÁREA DE DESENHO ---
        tela.fill((0,0,0))
        tela.blit(fundo_img, (0, 0))
        tela.blit(jogador_img, jogador['pos'])
        tela.blit(oponente_img, oponente['pos'])
        
        pos_y_ui = jogador['pos'][1] - 30
        texto_nome_jogador = fonte.render(jogador['nome'], True, BRANCO)
        tela.blit(texto_nome_jogador, (jogador['pos'][0], pos_y_ui - 30))
        desenhar_barra_hp(tela, jogador['pos'][0], pos_y_ui, jogador['hp_atual'], jogador['hp_max'])
        
        texto_nome_oponente = fonte.render(oponente['nome'], True, BRANCO)
        tela.blit(texto_nome_oponente, (oponente['pos'][0], pos_y_ui - 30))
        desenhar_barra_hp(tela, oponente['pos'][0], pos_y_ui, oponente['hp_atual'], oponente['hp_max'])
        
        desenhar_texto_quebra_linha(tela, mensagem_batalha, caixa_mensagem_rect, fonte_pequena, BRANCO)

        if not jogo_acabou:
            pygame.draw.rect(tela, CINZA_MINIMALISTA, botao_normal_rect)
            texto_botao_normal = fonte_pequena.render("Ataque Normal", True, BRANCO)
            tela.blit(texto_botao_normal, (botao_normal_rect.x + 22, botao_normal_rect.y + 12))
            pygame.draw.rect(tela, CINZA_MINIMALISTA, botao_critico_rect)
            texto_botao_critico = fonte_pequena.render("Ataque Crítico", True, BRANCO)
            tela.blit(texto_botao_critico, (botao_critico_rect.x + 20, botao_critico_rect.y + 12))
        else:
            pygame.draw.rect(tela, CINZA_MINIMALISTA, botao_voltar_rect)
            texto_voltar = fonte.render("Voltar ao Menu", True, BRANCO)
            tela.blit(texto_voltar, (botao_voltar_rect.x + 45, botao_voltar_rect.y + 10))

        pygame.display.flip()
        clock.tick(60)