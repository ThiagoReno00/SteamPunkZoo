# Arquivo: batalha.py
import pygame
import random
import threading
import time

# --- SEMÁFORO E EVENTO CUSTOMIZADO ---
dados_lock = threading.Semaphore(1)
OPONENTE_TERMINOU_TURNO = pygame.USEREVENT + 1

# --- FUNÇÕES AUXILIARES ---
def desenhar_barra_hp(tela, x, y, hp_atual, hp_maximo):
    if hp_atual < 0: hp_atual = 0
    LARGURA_BARRA, ALTURA_BARRA, COR_FUNDO, COR_FRENTE = 200, 20, (100, 0, 0), (0, 200, 0)
    if hp_maximo > 0: porcentagem_hp = hp_atual / hp_maximo
    else: porcentagem_hp = 0
    largura_hp_atual = LARGURA_BARRA * porcentagem_hp
    retangulo_fundo = pygame.Rect(x, y, LARGURA_BARRA, ALTURA_BARRA)
    retangulo_frente = pygame.Rect(x, y, largura_hp_atual, ALTURA_BARRA)
    pygame.draw.rect(tela, COR_FUNDO, retangulo_fundo)
    pygame.draw.rect(tela, COR_FRENTE, retangulo_frente)
    pygame.draw.rect(tela, (255,255,255), retangulo_fundo, 2)

def desenhar_texto_quebra_linha(tela, texto, rect, fonte, cor):
    superficie_caixa_msg = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    superficie_caixa_msg.fill((0, 0, 0, 150))
    tela.blit(superficie_caixa_msg, rect.topleft)
    palavras = texto.split(' '); linhas = []; linha_atual = ""
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
        tela.blit(texto_renderizado, (rect.x + 15, pos_y))
        pos_y += fonte.get_height()

def logica_oponente_thread(oponente, jogador, id_batalha):
    time.sleep(3)
    resultado_ataque = {}
    with dados_lock:
        if random.random() < 0.3:
            if random.random() < 0.5:
                dano = oponente['ataque_c']; mensagem = f"{oponente['nome']} usou um ataque CRÍTICO!"
            else:
                dano = 0; mensagem = f"{oponente['nome']} tentou um ataque crítico e errou!"
        else:
            if random.random() < 0.9:
                dano = oponente['ataque_n']; mensagem = f"{oponente['nome']} atacou e causou {dano} de dano!"
            else:
                dano = 0; mensagem = f"{oponente['nome']} errou o ataque!"
    resultado_ataque['dano'] = dano
    resultado_ataque['mensagem'] = mensagem
    evento_resultado = pygame.event.Event(OPONENTE_TERMINOU_TURNO, resultado=resultado_ataque, id_batalha=id_batalha)
    pygame.event.post(evento_resultado)


def tela_de_batalha(tela, dados_jogador_atual, dados_oponente, caminho_mapa_fundo):
    print("--- DEBUG (batalha.py): A FUNÇÃO tela_de_batalha FOI CHAMADA! ---")
    largura, altura = tela.get_size()
    BRANCO = (255, 255, 255)
    CINZA_MINIMALISTA = (80, 80, 80)
    
    try:
        fundo_img = pygame.image.load(caminho_mapa_fundo).convert()
        fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
        jogador_img_original = pygame.image.load(dados_jogador_atual["sprite_path"]).convert_alpha()
        oponente_img_original = pygame.image.load(dados_oponente["sprite_path"]).convert_alpha()
    except pygame.error as e:
        # NOSSA "BOMBA" DE DEBUG COM A INDENTAÇÃO CORRETA
        print("!!!!!!!!!! ERRO CAPTURADO AQUI !!!!!!!!!!!")
        print(f"O erro exato que o Pygame deu foi: {e}")
        raise # <-- Esta linha vai forçar o jogo a crashar e mostrar tudo

    jogador = dados_jogador_atual
    oponente = dados_oponente
    oponente['hp_atual'] = oponente['hp_max']
    jogador_img = pygame.transform.scale(jogador_img_original, jogador["tamanho"])
    oponente_img = pygame.transform.scale(oponente_img_original, oponente["tamanho"])
    margem_chao = 40
    margem_lateral = 100
    pos_y_jogador = altura - jogador['tamanho'][1] - margem_chao
    pos_y_oponente = altura - oponente['tamanho'][1] - margem_chao
    pos_x_jogador = margem_lateral
    pos_x_oponente = largura - oponente['tamanho'][0] - margem_lateral
    jogador['pos'] = (pos_x_jogador, pos_y_jogador)
    oponente['pos'] = (pos_x_oponente, pos_y_oponente)
    
    fonte = pygame.font.Font(None, 36)
    fonte_pequena = pygame.font.Font(None, 22)
    mensagem_batalha = f"Um(a) {oponente['nome']} selvagem apareceu!"
    altura_botao = 40
    largura_botao = 160
    margem_botoes = 20
    y_botoes = altura - altura_botao - margem_botoes
    x_botao_normal = margem_botoes
    x_botao_critico = margem_botoes + largura_botao + margem_botoes
    botao_normal_rect = pygame.Rect(x_botao_normal, y_botoes, largura_botao, altura_botao)
    botao_critico_rect = pygame.Rect(x_botao_critico, y_botoes, largura_botao, altura_botao)
    botao_voltar_rect = pygame.Rect(largura // 2 - 150, altura // 2, 300, 50)
    largura_caixa_msg=300
    altura_caixa_msg=100
    margem_caixa=20
    pos_x_caixa_msg=largura-largura_caixa_msg-margem_caixa
    pos_y_caixa_msg=altura-altura_caixa_msg-margem_caixa
    caixa_mensagem_rect = pygame.Rect(pos_x_caixa_msg, pos_y_caixa_msg, largura_caixa_msg, altura_caixa_msg)
    
    id_batalha_atual = random.randint(1, 1000000)
    turno_do_jogador = True
    oponente_esta_pensando = False
    jogo_acabou = False
    clock = pygame.time.Clock()
    
    rodando_batalha = True
    while rodando_batalha:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return {"resultado": "sair"}
            
            if evento.type == OPONENTE_TERMINOU_TURNO and evento.id_batalha == id_batalha_atual:
                with dados_lock:
                    resultado = evento.resultado
                    jogador['hp_atual'] -= resultado['dano']
                    mensagem_batalha = resultado['mensagem']
                    turno_do_jogador = True
                    oponente_esta_pensando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if turno_do_jogador and not jogo_acabou:
                    acao_realizada = False
                    with dados_lock:
                        if botao_normal_rect.collidepoint(evento.pos):
                            if random.random() < 0.9:
                                dano = jogador['ataque_n']
                                oponente['hp_atual'] -= dano
                                mensagem_batalha = f"{jogador['nome']} acertou e causou {dano} de dano!"
                            else:
                                mensagem_batalha = f"{jogador['nome']} errou o ataque!"
                            acao_realizada = True
                        elif botao_critico_rect.collidepoint(evento.pos):
                            if random.random() < 0.5:
                                dano = jogador['ataque_c']
                                oponente['hp_atual'] -= dano
                                mensagem_batalha = f"CRÍTICO! {jogador['nome']} causou {dano} de dano!"
                            else:
                                mensagem_batalha = f"{jogador['nome']} tentou um ataque crítico e errou!"
                            acao_realizada = True
                    if acao_realizada:
                        turno_do_jogador = False
                        oponente_esta_pensando = True
                
                if jogo_acabou and botao_voltar_rect.collidepoint(evento.pos):
                    if jogador['hp_atual'] > 0:
                        return {"resultado": "vitoria"}
                    else:
                        return {"resultado": "derrota"}

        if oponente_esta_pensando and 'thread_oponente' not in locals() or (oponente_esta_pensando and not thread_oponente.is_alive()):
            thread_oponente = threading.Thread(target=logica_oponente_thread, args=(oponente, jogador, id_batalha_atual))
            thread_oponente.start()
        
        with dados_lock:
            if oponente['hp_atual'] <= 0 and not jogo_acabou:
                oponente['hp_atual'] = 0
                mensagem_batalha = "VOCÊ VENCEU!"
                jogo_acabou = True
            if jogador['hp_atual'] <= 0 and not jogo_acabou:
                jogador['hp_atual'] = 0
                mensagem_batalha = "VOCÊ PERDEU!"
                jogo_acabou = True
        
        with dados_lock:
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
                texto_voltar = fonte.render("Continuar", True, BRANCO)
                tela.blit(texto_voltar, (botao_voltar_rect.centerx - texto_voltar.get_width() // 2, botao_voltar_rect.centery - texto_voltar.get_height() // 2))

        pygame.display.flip()
        
        if jogo_acabou:
            pygame.time.wait(2000)
            if jogador['hp_atual'] > 0:
                return {"resultado": "vitoria"}
            else:
                return {"resultado": "derrota"}

        clock.tick(60)
