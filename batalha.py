# Arquivo: batalha.py
import pygame
import random
import threading
import time
import math

# --- SEMÁFORO E EVENTO CUSTOMIZADO ---
dados_lock = threading.Semaphore(1)
OPONENTE_TERMINOU_TURNO = pygame.USEREVENT + 1

# --- FUNÇÕES AUXILIARES ---
def desenhar_barra_hp(tela_logica, x, y, hp_atual, hp_maximo):
    if hp_atual < 0: hp_atual = 0
    LARGURA_BARRA, ALTURA_BARRA, COR_FUNDO, COR_FRENTE = 200, 20, (100, 0, 0), (0, 200, 0)
    if hp_maximo > 0: porcentagem_hp = hp_atual / hp_maximo
    else: porcentagem_hp = 0
    largura_hp_atual = LARGURA_BARRA * porcentagem_hp
    retangulo_fundo = pygame.Rect(x, y, LARGURA_BARRA, ALTURA_BARRA)
    retangulo_frente = pygame.Rect(x, y, largura_hp_atual, ALTURA_BARRA)
    pygame.draw.rect(tela_logica, COR_FUNDO, retangulo_fundo)
    pygame.draw.rect(tela_logica, COR_FRENTE, retangulo_frente)
    pygame.draw.rect(tela_logica, (255,255,255), retangulo_fundo, 2)

def desenhar_texto_quebra_linha(tela_logica, texto, rect, fonte, cor):
    superficie_caixa_msg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    superficie_caixa_msg.fill((0, 0, 0, 150))
    tela_logica.blit(superficie_caixa_msg, rect.topleft)
    palavras = texto.split(' ')
    linhas = []
    linha_atual = ""
    margem = 30
    for palavra in palavras:
        teste_linha = linha_atual + palavra + " "
        if fonte.size(teste_linha)[0] < rect.width - margem:
            linha_atual = teste_linha
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)
    pos_y = rect.y + 15
    for linha in linhas:
        texto_renderizado = fonte.render(linha, True, cor)
        tela_logica.blit(texto_renderizado, (rect.x + 15, pos_y))
        pos_y += fonte.get_height()

def desenhar_texto_com_contorno(surface, texto, fonte, pos, cor_principal, cor_contorno):
    texto_surface = fonte.render(texto, True, cor_principal)
    contorno_surface = fonte.render(texto, True, cor_contorno)
    deslocamento = 2
    surface.blit(contorno_surface, (pos[0] - deslocamento, pos[1]))
    surface.blit(contorno_surface, (pos[0] + deslocamento, pos[1]))
    surface.blit(contorno_surface, (pos[0], pos[1] - deslocamento))
    surface.blit(contorno_surface, (pos[0], pos[1] + deslocamento))
    surface.blit(texto_surface, pos)

def logica_oponente_thread(oponente, jogador, id_batalha):
    time.sleep(3)
    resultado_ataque = {}
    with dados_lock:
        if random.random() < 0.3:
            if random.random() < 0.65:
                dano = oponente['ataque_c']
                mensagem = f"{oponente['nome']} usou um ataque CRÍTICO!"
            else:
                dano = 0
                mensagem = f"{oponente['nome']} tentou um ataque crítico e errou!"
        else:
            if random.random() < 0.95:
                dano = oponente['ataque_n']
                mensagem = f"{oponente['nome']} atacou e causou {dano} de dano!"
            else:
                dano = 0
                mensagem = f"{oponente['nome']} errou o ataque!"
    resultado_ataque['dano'] = dano
    resultado_ataque['mensagem'] = mensagem
    evento_resultado = pygame.event.Event(OPONENTE_TERMINOU_TURNO, resultado=resultado_ataque, id_batalha=id_batalha)
    pygame.event.post(evento_resultado)


def tela_de_batalha(tela_logica, tela_real, dados_jogador_atual, dados_oponente, caminho_mapa_fundo):
    largura, altura = tela_logica.get_size()
    LARGURA_REAL, ALTURA_REAL = tela_real.get_size()
    BRANCO = (255, 255, 255); CINZA_MINIMALISTA = (80, 80, 80); PRETO = (0, 0, 0)
    
    VELOCIDADE_RESPIRACAO = 0.003
    INTENSIDADE_RESPIRACAO = 0.02
    
    try:
        fundo_img = pygame.image.load(caminho_mapa_fundo).convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
        jogador_img_original = pygame.image.load(dados_jogador_atual["sprite_path"]).convert_alpha()
        oponente_img_original = pygame.image.load(dados_oponente["sprite_path"]).convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar imagem na batalha: {e}")
        return {"resultado": "derrota"}

    jogador = dados_jogador_atual
    oponente = dados_oponente
    oponente['hp_atual'] = oponente['hp_max']
    jogador.update({"foi_atingido": False, "tempo_hit": 0, "esta_atacando": False, "tempo_ataque": 0})
    oponente.update({"foi_atingido": False, "tempo_hit": 0, "esta_atacando": False, "tempo_ataque": 0})
    
    margem_chao = 40; margem_lateral = 100
    pos_y_ancora = altura - margem_chao
    pos_x_jogador_ancora = margem_lateral + (jogador['tamanho'][0] // 2)
    pos_x_oponente_ancora = largura - margem_lateral - (oponente['tamanho'][0] // 2)
    jogador['pos_ancora'] = (pos_x_jogador_ancora, pos_y_ancora)
    oponente['pos_ancora'] = (pos_x_oponente_ancora, pos_y_ancora)
    
    fonte = pygame.font.Font(None, 36); fonte_pequena = pygame.font.Font(None, 22)
    mensagem_batalha = f"Um(a) {oponente['nome']} selvagem apareceu!"
    altura_botao=40; largura_botao=160; margem_botoes=20; y_botoes=altura-altura_botao-margem_botoes
    x_botao_normal=margem_botoes; x_botao_critico=margem_botoes+largura_botao+margem_botoes
    botao_normal_rect = pygame.Rect(x_botao_normal, y_botoes, largura_botao, altura_botao)
    botao_critico_rect = pygame.Rect(x_botao_critico, y_botoes, largura_botao, altura_botao)
    botao_voltar_rect = pygame.Rect(largura // 2 - 150, altura // 2, 300, 50)
    largura_caixa_msg=300; altura_caixa_msg=100; margem_caixa=20
    pos_x_caixa_msg=largura-largura_caixa_msg-margem_caixa; pos_y_caixa_msg=altura-altura_caixa_msg-margem_caixa
    caixa_mensagem_rect = pygame.Rect(pos_x_caixa_msg, pos_y_caixa_msg, largura_caixa_msg, altura_caixa_msg)
    
    id_batalha_atual = random.randint(1, 1000000)
    turno_do_jogador = True; oponente_esta_pensando = False; jogo_acabou = False
    clock = pygame.time.Clock()
    
    rodando_batalha = True
    while rodando_batalha:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: return {"resultado": "sair"}
            
            if evento.type == OPONENTE_TERMINOU_TURNO and evento.id_batalha == id_batalha_atual:
                with dados_lock:
                    resultado = evento.resultado
                    if resultado['dano'] > 0: jogador['foi_atingido'] = True; jogador['tempo_hit'] = pygame.time.get_ticks()
                    jogador['hp_atual'] -= resultado['dano']; mensagem_batalha = resultado['mensagem']
                    turno_do_jogador = True; oponente_esta_pensando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_real, mouse_y_real = evento.pos
                escala_x = largura / LARGURA_REAL
                escala_y = altura / ALTURA_REAL
                pos_mouse_logico = (mouse_x_real * escala_x, mouse_y_real * escala_y)
                
                if turno_do_jogador and not jogo_acabou:
                    acao_realizada = False; dano = 0
                    with dados_lock:
                        if botao_normal_rect.collidepoint(pos_mouse_logico) or botao_critico_rect.collidepoint(pos_mouse_logico):
                            jogador['esta_atacando'] = True; jogador['tempo_ataque'] = pygame.time.get_ticks()
                            if botao_normal_rect.collidepoint(pos_mouse_logico):
                                if random.random() < 0.9: dano = jogador['ataque_n']; mensagem_batalha = f"{jogador['nome']} acertou e causou {dano} de dano!"
                                else: mensagem_batalha = f"{jogador['nome']} errou o ataque!"
                            elif botao_critico_rect.collidepoint(pos_mouse_logico):
                                if random.random() < 0.5: dano = jogador['ataque_c']; mensagem_batalha = f"CRÍTICO! {jogador['nome']} causou {dano} de dano!"
                                else: mensagem_batalha = f"{jogador['nome']} tentou um ataque crítico e errou!"
                            if dano > 0: oponente['hp_atual'] -= dano; oponente['foi_atingido'] = True; oponente['tempo_hit'] = pygame.time.get_ticks()
                            acao_realizada = True
                    if acao_realizada: turno_do_jogador = False; oponente_esta_pensando = True
                
                if jogo_acabou and botao_voltar_rect.collidepoint(pos_mouse_logico):
                    if jogador['hp_atual'] > 0: return {"resultado": "vitoria"}
                    else: return {"resultado": "derrota"}

        if oponente_esta_pensando and 'thread_oponente' not in locals() or (oponente_esta_pensando and not thread_oponente.is_alive()):
            with dados_lock: oponente['esta_atacando'] = True; oponente['tempo_ataque'] = pygame.time.get_ticks()
            thread_oponente = threading.Thread(target=logica_oponente_thread, args=(oponente, jogador, id_batalha_atual))
            thread_oponente.start()
        
        with dados_lock:
            if oponente['hp_atual'] <= 0 and not jogo_acabou: oponente['hp_atual'] = 0; mensagem_batalha = "VOCÊ VENCEU!"; jogo_acabou = True
            if jogador['hp_atual'] <= 0 and not jogo_acabou: jogador['hp_atual'] = 0; mensagem_batalha = "VOCÊ PERDEU!"; jogo_acabou = True
        
        with dados_lock:
            tela_logica.fill((0,0,0)); tela_logica.blit(fundo_img, (0, 0))

            onda_seno = math.sin(pygame.time.get_ticks() * VELOCIDADE_RESPIRACAO)
            escala_respiracao = 1 + (onda_seno * INTENSIDADE_RESPIRACAO)
            DURACAO_PISCA = 400; ALPHA_PISCA = 80; DURACAO_ATAQUE = 400; DISTANCIA_ATAQUE = 30
            
            # Desenho do Jogador
            tamanho_base_jogador = jogador['tamanho']; tamanho_atual_jogador = (int(tamanho_base_jogador[0] * escala_respiracao), int(tamanho_base_jogador[1] * escala_respiracao))
            jogador_img_redimensionada = pygame.transform.scale(jogador_img_original, tamanho_atual_jogador)
            jogador_rect = jogador_img_redimensionada.get_rect(midbottom=jogador['pos_ancora'])
            if jogador['esta_atacando']:
                tempo_passado = pygame.time.get_ticks() - jogador['tempo_ataque']
                if tempo_passado < DURACAO_ATAQUE:
                    if tempo_passado < DURACAO_ATAQUE / 2: jogador_rect.x += DISTANCIA_ATAQUE
                else: jogador['esta_atacando'] = False
            if jogador['foi_atingido']:
                tempo_passado = pygame.time.get_ticks() - jogador['tempo_hit']
                if tempo_passado > DURACAO_PISCA: jogador['foi_atingido'] = False
                elif tempo_passado // 100 % 2 == 0: jogador_img_redimensionada.set_alpha(ALPHA_PISCA)
                else: jogador_img_redimensionada.set_alpha(255)
            else: jogador_img_redimensionada.set_alpha(255)
            tela_logica.blit(jogador_img_redimensionada, jogador_rect)
            
            # Desenho do Oponente
            tamanho_base_oponente = oponente['tamanho']; tamanho_atual_oponente = (int(tamanho_base_oponente[0] * escala_respiracao), int(tamanho_base_oponente[1] * escala_respiracao))
            oponente_img_redimensionada = pygame.transform.scale(oponente_img_original, tamanho_atual_oponente)
            oponente_rect = oponente_img_redimensionada.get_rect(midbottom=oponente['pos_ancora'])
            if oponente['esta_atacando']:
                tempo_passado = pygame.time.get_ticks() - oponente['tempo_ataque']
                if tempo_passado < DURACAO_ATAQUE:
                    if tempo_passado < DURACAO_ATAQUE / 2: oponente_rect.x -= DISTANCIA_ATAQUE
                else: oponente['esta_atacando'] = False
            if oponente['foi_atingido']:
                tempo_passado = pygame.time.get_ticks() - oponente['tempo_hit']
                if tempo_passado > DURACAO_PISCA: oponente['foi_atingido'] = False
                elif tempo_passado // 100 % 2 == 0: oponente_img_redimensionada.set_alpha(ALPHA_PISCA)
                else: oponente_img_redimensionada.set_alpha(255)
            else: oponente_img_redimensionada.set_alpha(255)
            tela_logica.blit(oponente_img_redimensionada, oponente_rect)

            # Desenho da UI com nomes contornados
            barra_hp_y_jogador = jogador_rect.top - 25
            desenhar_barra_hp(tela_logica, jogador_rect.left, barra_hp_y_jogador, jogador['hp_atual'], jogador['hp_max'])
            texto_nome_render = fonte.render(jogador['nome'], True, BRANCO)
            nome_y_jogador = barra_hp_y_jogador - texto_nome_render.get_height() - 5
            desenhar_texto_com_contorno(tela_logica, jogador['nome'], fonte, (jogador_rect.left, nome_y_jogador), BRANCO, PRETO)
            
            barra_hp_y_oponente = oponente_rect.top - 25
            desenhar_barra_hp(tela_logica, oponente_rect.left, barra_hp_y_oponente, oponente['hp_atual'], oponente['hp_max'])
            texto_nome_oponente_render = fonte.render(oponente['nome'], True, BRANCO)
            nome_y_oponente = barra_hp_y_oponente - texto_nome_oponente_render.get_height() - 5
            desenhar_texto_com_contorno(tela_logica, oponente['nome'], fonte, (oponente_rect.left, nome_y_oponente), BRANCO, PRETO)
            
            desenhar_texto_quebra_linha(tela_logica, mensagem_batalha, caixa_mensagem_rect, fonte_pequena, BRANCO)
            if not jogo_acabou:
                pygame.draw.rect(tela_logica, CINZA_MINIMALISTA, botao_normal_rect); texto_botao_normal = fonte_pequena.render("Ataque Normal", True, BRANCO); tela_logica.blit(texto_botao_normal, (botao_normal_rect.x + 22, botao_normal_rect.y + 12))
                pygame.draw.rect(tela_logica, CINZA_MINIMALISTA, botao_critico_rect); texto_botao_critico = fonte_pequena.render("Ataque Crítico", True, BRANCO); tela_logica.blit(texto_botao_critico, (botao_critico_rect.x + 20, botao_critico_rect.y + 12))
            else:
                pygame.draw.rect(tela_logica, CINZA_MINIMALISTA, botao_voltar_rect); texto_voltar = fonte.render("Continuar", True, BRANCO); tela_logica.blit(texto_voltar, (botao_voltar_rect.centerx - texto_voltar.get_width() // 2, botao_voltar_rect.centery - texto_voltar.get_height() // 2))

        # Projeção para tela cheia
        tela_projetada = pygame.transform.scale(tela_logica, (LARGURA_REAL, ALTURA_REAL))
        tela_real.blit(tela_projetada, (0, 0))
        
        pygame.display.flip()
        
        if jogo_acabou:
            pygame.time.wait(2000)
            if jogador['hp_atual'] > 0: return {"resultado": "vitoria"}
            else: return {"resultado": "derrota"}

        clock.tick(60)
