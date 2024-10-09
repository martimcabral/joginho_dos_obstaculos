import pygame
import random

pygame.init()

# Cores ⬛⬜
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Tamanho da Janela
window_size = (720, 720)
janela = pygame.display.set_mode(window_size)
pygame.display.set_caption("ROCK AND STONE")

# Tamanho do player e a posicao de inicio
jogador_largura = 35
jogador_altura = 35
pocisao_x = window_size[0] // 2 - jogador_largura // 2
jog_y = window_size[1] - jogador_altura - 10

# Dimensoes dos obstaculos e a sua velocidade
obstaculo_largura = 35
obstaculo_altura = 35
obstaculo_speed = 4
obstaculos = []

# Fonte dos displays
font = pygame.font.Font(None, 30)

# Variaveis
score = 0
vidas = 5
vidas_max = 5

# Mete o controlo da frame rate ao clock
clock = pygame.time.Clock()

# Paths das Imagens
background_image_path = "background.png"
jogador_image_path = "duck.png"
ficsit_path = "ficsit.png"
maca_dourada_path = "golden_apple.png"
godot_path = "godot.png"

# Paths dos Sons:
ficsite_hit_sound_path = "red_hit.mp3"
maca_dourada_sound_path = "eating.mp3"
godot_hit_sound_path = "more_score.mp3"
background_hit_sound = "aria_math.mp3"

# Imagens:
background_image = pygame.transform.scale(pygame.image.load(background_image_path), window_size)
jogador_image = pygame.transform.scale(pygame.image.load(jogador_image_path), (jogador_largura, jogador_altura))
ficist_image = pygame.transform.scale(pygame.image.load(ficsit_path), (obstaculo_largura, obstaculo_altura))
maca_dourada_image = pygame.transform.scale(pygame.image.load(maca_dourada_path), (obstaculo_largura, obstaculo_altura))
gold_obstaculo_image = pygame.transform.scale(pygame.image.load(godot_path), (obstaculo_largura, obstaculo_altura))

# Sons:
ficsit_hit_sound = pygame.mixer.Sound(ficsite_hit_sound_path)
maca_dourada_sound = pygame.mixer.Sound(maca_dourada_sound_path)
godot_hit_sound = pygame.mixer.Sound(godot_hit_sound_path)

# Carrega a musca de fundo e faz-la em loop em mete em volume reduzido
pygame.mixer.music.load(background_hit_sound)
pygame.mixer.music.set_volume(0.8)  # Ajusta o volume (0.0 até 1.0)
pygame.mixer.music.play(-1)  # Loop 

# Variável para controlar a orientação do jogador
flipped = True

# Limite de movimento para cima
limite_superior = jog_y - 100

# Loop Principal
emJogo = True
while emJogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            emJogo = False
    
    # Mover o Player para os lados
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and pocisao_x > 0:
        pocisao_x -= 3
        flipped = False
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and pocisao_x < window_size[0] - jogador_largura:
        pocisao_x += 3
        flipped = True
    
    # Mover o Player para cima e baixo
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and jog_y > limite_superior:
        jog_y -= 3
    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and jog_y < window_size[1] - jogador_altura:
        jog_y += 3

    # Meter os obstaculos sempre pra baixo
    for obstaculo in obstaculos:
        obstaculo[1] += obstaculo_speed

    # Criar obstaculos constantemente
    if len(obstaculos) == 0 or obstaculos[-1][1] > 35:
        x = random.randint(0, window_size[0] - obstaculo_largura)
        tipo_obstaculo = random.choices([1, 2, 3, 4, 5], [5, 1, 1, 0.1, 0.05])[0]
        obstaculos.append([x, -obstaculo_altura, tipo_obstaculo])  # Add new obstacle

    # Remover obstaculos "fora da tela"
    if obstaculos and obstaculos[0][1] > window_size[1]:
        obstaculos.pop(0)

    # Verificar colisoes entre o player e os obstaculos
    for obstaculo in obstaculos:
        if pocisao_x < obstaculo[0] + obstaculo_largura and pocisao_x + jogador_largura > obstaculo[0] and \
            jog_y < obstaculo[1] + obstaculo_altura and jog_y + jogador_altura > obstaculo[1]:
            if obstaculo[2] == 4:  # Obstaculo verde aumenta a vida
                if vidas < vidas_max:
                    vidas += 1  
                obstaculos.remove(obstaculo)
                maca_dourada_sound.play()
            elif obstaculo[2] == 5:  # Obstaculo amarelo aumenta a pontuação 
                score += 1500  # em 1500
                obstaculos.remove(obstaculo)
                godot_hit_sound.play()
            else:  
                vidas -= 1  
                obstaculos.remove(obstaculo)
                ficsit_hit_sound.play()
                if vidas == 0:  # quando a vida chega a 0 termina o jogo
                    emJogo = False
    
    # Aumenta o score
    score += 1
    
    # "Desenhar" tudo na tela
    janela.blit(background_image, (0, 0)) 
    
    for obstaculo in obstaculos:
        if obstaculo[2] == 4:
            janela.blit(maca_dourada_image, (obstaculo[0], obstaculo[1]))
        elif obstaculo[2] == 5:
            janela.blit(gold_obstaculo_image, (obstaculo[0], obstaculo[1]))
        else:
            janela.blit(ficist_image, (obstaculo[0], obstaculo[1]))

    # Desenhar o jogador com flip se necessário
    if flipped:
        jogador_image_flipped = pygame.transform.flip(jogador_image, True, False)
        janela.blit(jogador_image_flipped, (pocisao_x, jog_y))
    else:
        janela.blit(jogador_image, (pocisao_x, jog_y))
    
    # Mostrar Pontuação e Vida
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    vidas_text = font.render(f"Vidas: {vidas}", True, WHITE)
    janela.blit(score_text, (window_size[0] // 2 - score_text.get_width() // 2, 20))
    janela.blit(vidas_text, (20, 20))

    pygame.display.update()
    
    # Controlar a frame rate
    clock.tick(120)  

# Sair do jogo e mostrar a pontuação e termina a musca
pygame.mixer.music.stop()
pygame.quit()
print("Pontuação final: ", score)
