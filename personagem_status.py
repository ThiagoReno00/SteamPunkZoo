# Arquivo: personagens_status.py

PERSONAGENS_BASE = {
    "Urso": {
        "icone_path": "icone_urso.png",
        "evolucoes": [
            # Nomes e status balanceados, mas o sprite_path é o seu original.
            {"nome": "Urso de Bronze", "sprite_path": "urso.png", "hp_max": 160, "ataque_n": 20, "ataque_c": 32, "tamanho": (260, 260)},
            {"nome": "Urso de Aço", "sprite_path": "urso_evoluido.png", "hp_max": 220, "ataque_n": 26, "ataque_c": 42, "tamanho": (290, 290)},
            {"nome": "Urso de Titânio", "sprite_path": "urso_final.png", "hp_max": 300, "ataque_n": 32, "ataque_c": 55, "tamanho": (330, 330)}
        ]
    },
    "Raposa": {
        "icone_path": "icone_raposa.png",
        "evolucoes": [
            {"nome": "Raposa Astuta", "sprite_path": "raposa.png", "hp_max": 100, "ataque_n": 19, "ataque_c": 40, "tamanho": (190, 190)},
            {"nome": "Raposa Sônica", "sprite_path": "raposa_evoluida.png", "hp_max": 140, "ataque_n": 26, "ataque_c": 58, "tamanho": (210, 210)},
            {"nome": "Kitsune Fantasma", "sprite_path": "raposa_final.png", "hp_max": 180, "ataque_n": 34, "ataque_c": 75, "tamanho": (230, 230)}
        ]
    },
    "Tigre": {
        "icone_path": "icone_tigre.png",
        "evolucoes": [
            # Mantendo seus caminhos originais para as evoluções do Tigre
            {"nome": "Tigre Feroz", "sprite_path": "tigre_inicial.png", "hp_max": 110, "ataque_n": 18, "ataque_c": 35, "tamanho": (250, 210)},
            {"nome": "Tigre Dentes-de-Sabre", "sprite_path": "tigre.png", "hp_max": 160, "ataque_n": 25, "ataque_c": 50, "tamanho": (280, 240)},
            {"nome": "Tigre Avatar", "sprite_path": "tigre_final.png", "hp_max": 210, "ataque_n": 32, "ataque_c": 65, "tamanho": (310, 270)}
        ]
    },
    "Pinguim": {
        "icone_path": "icone_pinguim.png",
        "evolucoes": [
            {"nome": "Pinguim Tático", "sprite_path": "pinguim_inicial.png", "hp_max": 120, "ataque_n": 16, "ataque_c": 30, "tamanho": (140, 140)},
            {"nome": "Pinguim Comandante", "sprite_path": "pinguim.png", "hp_max": 170, "ataque_n": 22, "ataque_c": 40, "tamanho": (160, 160)},
            {"nome": "Pinguim Imperador", "sprite_path": "pinguim_final.png", "hp_max": 240, "ataque_n": 28, "ataque_c": 52, "tamanho": (240, 240)}
        ]
    },
    "Iguana": {
        "icone_path": "icone_iguana.png",
        "evolucoes": [
            {"nome": "Iguana Blindada", "sprite_path": "iguana_inicial.png", "hp_max": 115, "ataque_n": 17, "ataque_c": 33, "tamanho": (210, 160)},
            {"nome": "Iguana de Guerra", "sprite_path": "iguana.png", "hp_max": 160, "ataque_n": 23, "ataque_c": 45, "tamanho": (240, 190)},
            {"nome": "Dragão de Aço", "sprite_path": "iguana_final.png", "hp_max": 210, "ataque_n": 29, "ataque_c": 58, "tamanho": (270, 220)}
        ]
    },
    "Ganso": {
        "icone_path": "icone_ganso.png",
        "evolucoes": [
            {"nome": "Ganso Foguete", "sprite_path": "ganso_inicial.png", "hp_max": 80, "ataque_n": 12, "ataque_c": 50, "tamanho": (160, 160)},
            {"nome": "Ganso do Caos", "sprite_path": "ganso.png", "hp_max": 110, "ataque_n": 16, "ataque_c": 65, "tamanho": (180, 180)},
            {"nome": "O GANSOCALIPSE", "sprite_path": "ganso_final.png", "hp_max": 140, "ataque_n": 20, "ataque_c": 90, "tamanho": (200, 200)}
        ]
    },
    
    # --- OPONENTES ---
    "Aranha de Ferro": {
        "icone_path": "oponente_1.png",
        "evolucoes": [{"nome": "Aranha de Ferro", "sprite_path": "oponente_1.png", "hp_max": 100, "ataque_n": 15, "ataque_c": 25, "tamanho": (250, 250)}]
    },
    "Robo Medio": {
        "icone_path": "oponente_2.png",
        "evolucoes": [{"nome": "Mario Fumaça", "sprite_path": "oponente_2.png", "hp_max": 160, "ataque_n": 20, "ataque_c": 35, "tamanho": (280, 280)}]
    },
    "Robo Grande": {
        "nome": "Robo Grande",
        "icone_path": "oponente_3.png",
        "evolucoes": [{"nome": "Gordão de Ferro", "sprite_path": "oponente_3.png", "hp_max": 230, "ataque_n": 25, "ataque_c": 45, "tamanho": (350, 350)}]
    }
}
