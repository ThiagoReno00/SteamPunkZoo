# Arquivo: personagens_status.py

PERSONAGENS_BASE = {
    # --- A LINHA EVOLUTIVA DO URSO ---
    "Urso": {
        "icone_path": "icone_urso.png", # O ícone na seleção é sempre o mesmo
        "evolucoes": [
            # Estágio 1 (Base)
            {"nome": "Urso", "sprite_path": "urso.png", "hp_max": 120, "ataque_n": 100, "ataque_c": 25, "tamanho": (150, 150)},
            # Estágio 2 (Evolução)
            {"nome": "Urso Biônico", "sprite_path": "urso_evoluido.png", "hp_max": 180, "ataque_n": 100, "ataque_c": 40, "tamanho": (250, 250)},
            # Estágio 3 (Final)
            {"nome": "Urso Titã", "sprite_path": "urso_final.png", "hp_max": 250, "ataque_n": 20, "ataque_c": 100, "tamanho": (350, 350)}
        ]
    },
    
    # --- OUTROS PERSONAGENS (com estrutura de evolução, mas apenas 1 estágio) ---
    "Raposa": {
        "icone_path": "icone_raposa.png",
        "evolucoes": [
            {"nome": "Raposa", "sprite_path": "raposa.png", "hp_max": 80, "ataque_n": 15, "ataque_c": 30, "tamanho": (220, 220)}
        ]
    },
    "Ganso": {
        "icone_path": "icone_ganso.png",
        "evolucoes": [
            {"nome": "Ganso", "sprite_path": "ganso.png", "hp_max": 70, "ataque_n": 18, "ataque_c": 35, "tamanho": (170, 170)}
        ]
    },
    # Oponentes também seguem a mesma estrutura
    "Aranha de Ferro": {
        "icone_path": "oponente_1.png",
        "evolucoes": [
            {"nome": "Aranha de Ferro", "sprite_path": "oponente_1.png", "hp_max": 100, "ataque_n": 20, "ataque_c": 30, "tamanho": (170, 170)}
        ]
    },
    "Robo Medio": {
        "icone_path": "oponente_2.png",
        "evolucoes": [
            {"nome": "Robo Medio", "sprite_path": "oponente_2.png", "hp_max": 150, "ataque_n": 15, "ataque_c": 25, "tamanho": (280, 280)}
        ]
    },
    "Robo Grande": {
        "icone_path": "oponente_3.png",
        "evolucoes": [
            {"nome": "Robo Grande", "sprite_path": "oponente_3.png", "hp_max": 200, "ataque_n": 12, "ataque_c": 35, "tamanho": (420, 420)}
        ]
    }
    # Adicione os outros personagens que você criou aqui, seguindo o mesmo modelo
}
