import pygame

pygame.init()

largura, altura = 1024, 487
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Primeiro Jogo")

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    cor_de_fundo = (30, 30, 30)
    tela.fill(cor_de_fundo)
    pygame.display.flip()
    
pygame.quit()