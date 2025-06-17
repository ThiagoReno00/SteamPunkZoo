# Arquivo: main.py
import pygame
import copy
from menu import tela_de_menu
from selecao_personagem import tela_selecao_personagem
from selecao_mapa import tela_selecao_mapa
from batalha import tela_de_batalha
from personagens_status import PERSONAGENS_BASE

def main():
    pygame.init()
    pygame.mixer.init()

    tela_real = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    LARGURA_LOGICA, ALTURA_LOGICA = 1024, 487
    tela_logica = pygame.Surface((LARGURA_LOGICA, ALTURA_LOGICA))

    pygame.display.set_caption("Batalha Animal - Campanha")

    estado_do_jogo = "menu"
    chave_jogador = None; dados_jogador = None; mapa_escolhido = None
    fase_atual = 1; musica_atual = None

    # Lista de fases agora só define a ordem dos oponentes
    FASES = [
        {"fase": 1, "oponente_id": "Aranha de Ferro"},
        {"fase": 2, "oponente_id": "Robo Medio"},
        {"fase": 3, "oponente_id": "Robo Grande"}
    ]
    
    rodando = True
    while rodando:
        if estado_do_jogo == "menu":
            if musica_atual != "menu":
                try: pygame.mixer.music.load('musica.mp3'); pygame.mixer.music.play(-1); musica_atual = "menu"
                except pygame.error as e: print(f"Erro: {e}"); musica_atual = "erro"
            resposta = tela_de_menu(tela_logica, tela_real)
            if resposta == "iniciar": estado_do_jogo = "selecao_personagem"; fase_atual = 1
            elif resposta == "sair": rodando = False

        elif estado_do_jogo == "selecao_personagem":
            chave_personagem_escolhido = tela_selecao_personagem(tela_logica, tela_real)
            if chave_personagem_escolhido:
                chave_jogador = chave_personagem_escolhido
                dados_jogador = copy.deepcopy(PERSONAGENS_BASE[chave_jogador]["evolucoes"][0])
                dados_jogador['hp_atual'] = dados_jogador['hp_max']
                estado_do_jogo = "selecao_mapa" 
            else: estado_do_jogo = "menu"
        
        elif estado_do_jogo == "selecao_mapa":
            mapa_escolhido = tela_selecao_mapa(tela_logica, tela_real)
            if mapa_escolhido: estado_do_jogo = "batalha"
            else: estado_do_jogo = "selecao_personagem"

        elif estado_do_jogo == "batalha":
            if musica_atual != "batalha":
                try: pygame.mixer.music.load('musica.mp3'); pygame.mixer.music.play(-1); musica_atual = "batalha"
                except pygame.error as e: print(f"Erro: {e}"); musica_atual = "erro"
            
            info_fase = FASES[fase_atual - 1]
            oponente_id = info_fase["oponente_id"]
            
            # --- CORREÇÃO FINAL ---
            # A variável 'mapa' agora usa a escolha do jogador, guardada em 'mapa_escolhido'
            mapa = mapa_escolhido
            
            dados_oponente_base = copy.deepcopy(PERSONAGENS_BASE[oponente_id]["evolucoes"][0])
            
            multiplicador = 1 + ((fase_atual - 1) * 0.2)
            dados_oponente_base['hp_max'] = int(dados_oponente_base['hp_max'] * multiplicador)
            dados_oponente_base['ataque_n'] = int(dados_oponente_base['ataque_n'] * multiplicador)
            dados_oponente_base['ataque_c'] = int(dados_oponente_base['ataque_c'] * multiplicador)

            resultado_batalha = tela_de_batalha(tela_logica, tela_real, dados_jogador, dados_oponente_base, mapa)

            if resultado_batalha["resultado"] == "vitoria":
                pygame.event.clear(); fase_atual += 1
                if fase_atual > len(FASES):
                    print("VOCÊ VENCEU O JOGO!"); estado_do_jogo = "menu"
                else:
                    indice_evolucao = min(fase_atual - 1, len(PERSONAGENS_BASE[chave_jogador]["evolucoes"]) - 1)
                    dados_jogador = copy.deepcopy(PERSONAGENS_BASE[chave_jogador]["evolucoes"][indice_evolucao])
                    dados_jogador['hp_atual'] = dados_jogador['hp_max']
                    print(f"VITÓRIA! O personagem evoluiu para {dados_jogador['nome']}! Indo para a fase {fase_atual}.")
                    estado_do_jogo = "batalha"
            else:
                pygame.event.clear()
                if resultado_batalha["resultado"] == "sair": rodando = False
                else: estado_do_jogo = "menu"
    
    pygame.quit()

if __name__ == '__main__':
    main()
