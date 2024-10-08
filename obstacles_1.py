import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

window_size = (720, 720)
janela = pygame.display.set_mode(window_size)
pygame.display.set_caption("ROCK AND STONE")

jogador_largura = 35
jog_altura = 35
pocisao_x = window_size[0] // 2 - jogador_largura // 2
pocisao_y = window_size[0] // 2 - jogador_largura // 2
jog_y = window_size[1] - jog_altura - 10

obstaculo_largura = 35
obstaculo_altura = 35
obstaculo_speed = 2
obstaculos = []

font = pygame.font.Font(None, 30)

score = 0
vidas = 10
vidas_max = 10

clock = pygame.time.Clock()

# Image paths
background_image_path = "background.png"
jogador_image_path = "duck.png"
red_obstaculo_image_path = "ficsit.png"
green_obstaculo_image_path = "golden_apple.png"
gold_obstaculo_image_path = "godot.png"

# Sound paths
red_hit_sound_path = "red_hit.mp3"
green_hit_sound_path = "eating.mp3"
gold_hit_sound_path = "more_score.mp3"

# Load images
background_image = pygame.transform.scale(pygame.image.load(background_image_path), window_size)
jogador_image = pygame.transform.scale(pygame.image.load(jogador_image_path), (jogador_largura, jog_altura))
red_obstaculo_image = pygame.transform.scale(pygame.image.load(red_obstaculo_image_path), (obstaculo_largura, obstaculo_altura))
green_obstaculo_image = pygame.transform.scale(pygame.image.load(green_obstaculo_image_path), (obstaculo_largura, obstaculo_altura))
gold_obstaculo_image = pygame.transform.scale(pygame.image.load(gold_obstaculo_image_path), (obstaculo_largura, obstaculo_altura))

# Load sounds
red_hit_sound = pygame.mixer.Sound(red_hit_sound_path)
green_hit_sound = pygame.mixer.Sound(green_hit_sound_path)
gold_hit_sound = pygame.mixer.Sound(gold_hit_sound_path)

emJogo = True
while emJogo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            emJogo = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and pocisao_x > 0:
        pocisao_x -= 3
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and pocisao_x < window_size[0] - jogador_largura:
        pocisao_x += 3
    
    if keys[pygame.K_UP] or keys[pygame.K_w] and pocisao_y > 0:
        pocisao_y -= 1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s] and pocisao_y < window_size[0] - jogador_largura:
        pocisao_y += 1
  
    for obstaculo in obstaculos:
        obstaculo[1] += obstaculo_speed

    if len(obstaculos) == 0 or obstaculos[-1][1] > 35:
        x = random.randint(0, window_size[0] - obstaculo_largura)
        tipo_obstaculo = random.choices([1, 2, 3, 4, 5], [5, 1, 1, 0.1, 0.05])[0]
        obstaculos.append([x, -obstaculo_altura, tipo_obstaculo])

    if obstaculos and obstaculos[0][1] > window_size[1]:
        obstaculos.pop(0)

    for obstaculo in obstaculos:
        if pocisao_x < obstaculo[0] + obstaculo_largura and pocisao_x + jogador_largura > obstaculo[0] and \
            jog_y < obstaculo[1] + obstaculo_altura and jog_y + jog_altura > obstaculo[1]:
            if obstaculo[2] == 4:
                if vidas < vidas_max:
                    vidas += 1
                obstaculos.remove(obstaculo)
                green_hit_sound.play()
            elif obstaculo[2] == 5:
                score += 1500
                obstaculos.remove(obstaculo)
                gold_hit_sound.play()
            else:
                vidas -= 1
                obstaculos.remove(obstaculo)
                red_hit_sound.play()
                if vidas == 0:
                    emJogo = False
    
    score += 1
    
    janela.blit(background_image, (0, 0))  # Draw background image
    
    for obstaculo in obstaculos:
        if obstaculo[2] == 4:
            janela.blit(green_obstaculo_image, (obstaculo[0], obstaculo[1]))
        elif obstaculo[2] == 5:
            janela.blit(gold_obstaculo_image, (obstaculo[0], obstaculo[1]))
        else:
            janela.blit(red_obstaculo_image, (obstaculo[0], obstaculo[1]))

    janela.blit(jogador_image, (pocisao_x, jog_y))
    
    score_text = font.render(f"Pontuação: {score}", True, WHITE)
    vidas_text = font.render(f"Vidas: {vidas}", True, WHITE)
    janela.blit(score_text, (window_size[0] // 2 - score_text.get_width() // 2, 20))
    janela.blit(vidas_text, (20, 20))

    pygame.display.update()

    clock.tick(144)

pygame.quit()
print("Pontuação final =", score)
