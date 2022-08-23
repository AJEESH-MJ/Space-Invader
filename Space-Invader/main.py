import math
import random
import pygame

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')
background_image = pygame.transform.scale(background, (800, 600))

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('number-one.png')
pygame.display.set_icon(icon)

# Player
player_Img = pygame.image.load('space-invaders.png')
player_image = pygame.transform.scale(player_Img, (64, 64))
player_X = 370
player_Y = 480
playerX_change = 0

# Enemy
enemyImg = []
enemy_X = []
enemy_Y = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemy_X.append(random.randint(0, 736))
    enemy_Y.append(random.randint(50, 100))
    enemyX_change.append(3)
    enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load('bullet.png')

bullet_X = 0
bullet_Y = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_X = 10
test_Y = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt(math.pow(enemy_X - bullet_X, 2) + (math.pow(enemy_Y - bullet_Y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_X = player_X
                    fire_bullet(bullet_X, bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    player_X += playerX_change
    if player_X <= 0:
        player_X = 0
    elif player_X >= 736:
        player_X = 736

    # Enemy Movement
    for i in range(number_of_enemies):

        # Game Over
        if enemy_Y[i] > 440:
            for j in range(number_of_enemies):
                enemy_Y[j] = 2000
            game_over_text()
            break

        enemy_X[i] += enemyX_change[i]
        if enemy_X[i] <= 0:
            enemyX_change[i] = 3
            enemy_Y[i] += enemyY_change[i]
        elif enemy_X[i] >= 736:
            enemyX_change[i] = -3
            enemy_Y[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        if collision:
            bullet_Y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 100)

        enemy(enemy_X[i], enemy_Y[i], i)

    # Bullet Movement
    if bullet_Y <= 0:
        bullet_Y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_X, bullet_Y)
        bullet_Y -= bulletY_change

    player(player_X, player_Y)
    show_score(text_X, test_Y)
    pygame.display.update()
