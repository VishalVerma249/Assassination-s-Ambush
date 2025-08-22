import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("Assassination's Ambush")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Background image
backgroundimage = pygame.image.load("backgroundimage.png")
backgroundimage = pygame.transform.scale(backgroundimage, (1000, 750))

# Background sound
mixer.music.load("backgrogund_music.wav")
mixer.music.play(-1)

# Font
font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 72)

# Player
playerimage = pygame.image.load("ninja.png")
playerimage = pygame.transform.scale(playerimage, (100, 100))

def playerlocation(y, x):
    screen.blit(playerimage, (y, x))
# Score
score_value = 0
textX = 50
textY = 50

def dispaly_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 0))
    screen.blit(score, (x, y))


# Enemy
enemyimage = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
if score_value>=5:
    num_of_enemy = 5
else:
    num_of_enemy=3

def create_enemies():
    enemyimage.clear()
    enemyX.clear()
    enemyY.clear()
    enemy_changeX.clear()
    enemy_changeY.clear()
    for i in range(num_of_enemy):
        enemyimg = pygame.image.load("enemy ninja.png")
        enemyimg = pygame.transform.scale(enemyimg, (100, 100))
        enemyimage.append(enemyimg)
        enemyX.append(random.randint(0, 888))
        enemyY.append(random.randint(0, 650))
        enemy_changeX.append(0.4)
        enemy_changeY.append(0.4)

def enemylocation(y, x, i):
    screen.blit(enemyimage[i], (y, x))

# Bullet
sukrikenimage = pygame.image.load("suriken.png")
sukrikenimage = pygame.transform.scale(sukrikenimage, (50, 50))
surikenX = 0
surikenY = 600
suriken_changeY = 2
suriken_state = "ready"

def fire_suriken(x, y):
    global suriken_state
    suriken_state = "fire"
    screen.blit(sukrikenimage, (x + 5, y + 2))


# Collision detection
def issuriken_hits(surikenX, surikenY, enemyX, enemyY):
    distance = math.sqrt((enemyX - surikenX)**2 + (enemyY - surikenY)**2)
    return distance < 35

def is_player_hit(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt((enemyX - playerX)**2 + (enemyY - playerY)**2)
    return distance < 50

def game_over_screen():
    while True:
        screen.fill((0, 0, 0))
        screen.blit(backgroundimage, (0, 0))

        over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render("Your Score: " + str(score_value), True, (255, 255, 255))
        play_again_text = font.render("[ PRESS ENTER TO PLAY AGAIN ]", True, (255, 255, 255))

        screen.blit(over_text, (300, 250))
        screen.blit(score_text, (380, 350))
        screen.blit(play_again_text, (270, 450))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Game loop
while True:
    # Initialize/reset variables
    playerx = 380
    playery = 600
    player_changey = 0
    player_changex = 0
    surikenX = 0
    surikenY = 600
    suriken_state = "ready"
    score_value = 0
    create_enemies()
    mixer.music.play(-1)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(backgroundimage, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_changex = -0.8
                if event.key == pygame.K_RIGHT:
                    player_changex = 0.8
                if event.key == pygame.K_DOWN:
                    player_changey = 0.8
                if event.key == pygame.K_UP:
                    player_changey = -0.8
                if event.key == pygame.K_SPACE:
                    if suriken_state == "ready":
                        suriken_sound = mixer.Sound("Thrown Shuriken.wav")
                        suriken_sound.play()
                        surikenX = playerx
                        surikenY = playery
                        fire_suriken(surikenX, surikenY)
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    player_changex = 0
                    player_changey = 0

        playerx += player_changex
        playery += player_changey
        playerx = max(0, min(888, playerx))
        playery = max(0, min(650, playery))

        playerlocation(playerx, playery)

        for i in range(num_of_enemy):
            enemyX[i] += enemy_changeX[i]
            enemyY[i] += enemy_changeY[i]

            if enemyX[i] <= 0 or enemyX[i] >= 888:
                enemy_changeX[i] *= -1
            if enemyY[i] <= 0 or enemyY[i] >= 650:
                enemy_changeY[i] *= -1

            enemylocation(enemyX[i], enemyY[i], i)

            if suriken_state == "fire" and issuriken_hits(surikenX, surikenY, enemyX[i], enemyY[i]):
                collision = mixer.Sound("impact.wav")
                collision.play()
                surikenY = 600
                suriken_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 888)
                enemyY[i] = random.randint(0, 650)

            if is_player_hit(playerx, playery, enemyX[i], enemyY[i]):
                mixer.music.stop()
                game_over_sound = mixer.Sound("impact.wav")
                game_over_sound.play()
                running = False

        if surikenY <= 0:
            surikenY = 600
            suriken_state = "ready"
        if suriken_state == "fire":
            fire_suriken(surikenX, surikenY)
            surikenY -= suriken_changeY

        dispaly_score(textX, textY)
        pygame.display.update()

    game_over_screen()
