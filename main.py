# Arquivo: main.py
import pygame
import copy
from menu import tela_de_menu
from selecao_personagem import tela_selecao_personagem
from batalha import tela_de_batalha
from personagens_status import PERSONAGENS_BASE

def main():
    pygame.init()
    pygame.mixer.init()

    largura, altura = 1024, 487
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Batalha Animal - Campanha")

    estado_do_jogo = "menu"
    chave_jogador = None # Guardará a "chave" do personagem (ex: "Urso")
    dados_jogador = None # Guardará os dados da evolução ATUAL
    mapa_escolhido = "cenario_floresta.jpg" # Mapa fixo por enquanto
    fase_atual = 1
    musica_atual = None

    FASES = [
        {"fase": 1, "oponente_id": "Aranha de Ferro"},
        {"fase": 2, "oponente_id": "Robo Medio"},
        {"fase": 3, "oponente_id": "Robo Grande"}
    ]

    while True:
        if estado_do_jogo == "menu":
            # ... (lógica do menu e música)
            if tela_de_menu(tela) == "iniciar":
                estado_do_jogo = "selecao_personagem"
                fase_atual = 1
            else:
                break

        elif estado_do_jogo == "selecao_personagem":
            chave_personagem_escolhido = tela_selecao_personagem(tela)
            if chave_personagem_escolhido:
                chave_jogador = chave_personagem_escolhido
                # --- PEGA A PRIMEIRA EVOLUÇÃO (ESTÁGIO BASE) ---
                dados_jogador = copy.deepcopy(PERSONAGENS_BASE[chave_jogador]["evolucoes"][0])
                dados_jogador['hp_atual'] = dados_jogador['hp_max']
                estado_do_jogo = "batalha"
            else:
                estado_do_jogo = "menu"
        
        elif estado_do_jogo == "batalha":
            # ... (lógica da música)
            
            info_fase = FASES[fase_atual - 1]
            oponente_id = info_fase["oponente_id"]
            
            # Pega a primeira (e única) forma do oponente
            dados_oponente_base = copy.deepcopy(PERSONAGENS_BASE[oponente_id]["evolucoes"][0])
            
            # (Aqui mantemos a evolução do oponente que tínhamos antes, se quiser tirar, comente as linhas)
            multiplicador = 1 + ((fase_atual - 1) * 0.25)
            dados_oponente_base['hp_max'] = int(dados_oponente_base['hp_max'] * multiplicador)
            dados_oponente_base['ataque_n'] = int(dados_oponente_base['ataque_n'] * multiplicador)
            dados_oponente_base['ataque_c'] = int(dados_oponente_base['ataque_c'] * multiplicador)

            resultado_batalha = tela_de_batalha(tela, dados_jogador, dados_oponente_base, mapa_escolhido)

            if resultado_batalha["resultado"] == "vitoria":
                pygame.event.clear()
                fase_atual += 1
                
                if fase_atual > len(FASES):
                    print("VOCÊ VENCEU O JOGO!")
                    estado_do_jogo = "menu"
                else:
                    # --- LÓGICA DA EVOLUÇÃO DO JOGADOR ---
                    # Pega a próxima evolução da lista. Usa min() para não dar erro se não houver mais evoluções
                    indice_evolucao = min(fase_atual - 1, len(PERSONAGENS_BASE[chave_jogador]["evolucoes"]) - 1)
                    
                    # Atualiza os dados do jogador com os da sua nova forma!
                    dados_jogador = copy.deepcopy(PERSONAGENS_BASE[chave_jogador]["evolucoes"][indice_evolucao])
                    dados_jogador['hp_atual'] = dados_jogador['hp_max'] # Cura total
                    
                    print(f"VITÓRIA! {dados_jogador['nome']} evoluiu! Indo para a fase {fase_atual}.")
                    estado_do_jogo = "batalha" # Continua para a próxima batalha
            
            else: # Derrota ou saiu
                pygame.event.clear()
                estado_do_jogo = "menu"
    
    pygame.quit()

if __name__ == '__main__':
    main()
