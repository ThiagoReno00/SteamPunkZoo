# Arquivo: main.py
import pygame
from menu import tela_de_menu
from selecao_personagem import tela_selecao_personagem # NOVO IMPORT
from selecao_mapa import tela_selecao_mapa           # NOVO IMPORT
from batalha import tela_de_batalha

def main():
    pygame.init()
    largura, altura = 1024, 487 # Ou o tamanho que você estiver usando
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Batalha Animal")

    estado_do_jogo = "menu"
    
    # Variáveis para guardar as escolhas
    personagem_escolhido = None
    mapa_escolhido = None

    while True:
        if estado_do_jogo == "menu":
            resposta = tela_de_menu(tela)
            if resposta == "iniciar":
                estado_do_jogo = "selecao_personagem" # Próximo estado
            elif resposta == "sair":
                break

        elif estado_do_jogo == "selecao_personagem":
            personagem_escolhido = tela_selecao_personagem(tela)
            if personagem_escolhido: # Se um personagem foi escolhido...
                estado_do_jogo = "selecao_mapa" # ...vá para a seleção de mapa
            else: # Se o jogador fechou a janela...
                estado_do_jogo = "menu" # ...volte para o menu principal

        elif estado_do_jogo == "selecao_mapa":
            mapa_escolhido = tela_selecao_mapa(tela)
            if mapa_escolhido: # Se um mapa foi escolhido...
                estado_do_jogo = "batalha" # ...vá para a batalha!
            else: # Se o jogador fechou a janela...
                estado_do_jogo = "selecao_personagem" # ...volte para a seleção de personagem

        elif estado_do_jogo == "batalha":
            # --- MUDANÇA: PASSA AS ESCOLHAS PARA A FUNÇÃO DE BATALHA ---
            resposta = tela_de_batalha(tela, personagem_escolhido, mapa_escolhido)
            if resposta == "voltar_menu":
                estado_do_jogo = "menu"
            elif resposta == "sair":
                break

    pygame.quit()

if __name__ == '__main__':
    main()