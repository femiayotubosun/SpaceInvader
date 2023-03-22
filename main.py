import pygame
import assets
import random
import math
from pygame import mixer

# Initialization
pygame.init()

# Set display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(assets.icon)

# Player
playerX = 390
playerY = 540
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(assets.player_img, (x, y))


# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
default_enemy_x_change = 0.5

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(assets.enemy_img)
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)


def enemy(x, y):
    screen.blit(assets.enemy_img, (x, y))


# Music
hit_sound = mixer.Sound('./assets/explosion.wav')

# Bullet
# Ready you can't see the bullet
# Fire, the bullet is moving
bulletX = 390
bulletY = 540
bulletX_change = 0
bulletY_change = -0.5
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 22)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

text_x = 10
text_y = 10


def show_score(x, y):
    score_text = f"Score: {score_value}"
    score = font.render(score_text, True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 350))


bullets = []


# def fire_bullet():
#     global bullet_state
#     bullet_state = "fire"
#     screen.blit(assets.bullet, (x + 8, y + 10))


def spawn_bullet():
    newBullet = Bullet()
    newBullet.state = "fire"
    bullets.append(newBullet)


def bullet(x, y):
    screen.blit(assets.bullet, (x, y))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))

    return distance < 27


class Bullet:
    def __init__(self, img=assets.bullet):
        self.y = playerY + 10
        self.img = img
        self.x = playerX + 8
        self.state = "ready"

    def display(self):
        screen.blit(self.img, (self.x, self.y))

    def set_y(self, y):
        self.y = y;


# Game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(assets.background, (0, 0))
    # All events are logged in here.
    """
    All events are logged in .event.get().
    Here we define our event handlers.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and playerX != 0:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT and playerX != 760:
                playerX_change = 0.3

            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                spawn_bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Increase any speed on mileston
    if score_value == 10 == 0:
        default_enemyX_change = 0.5

    # Checking for boundaries of artifacts, so they don't go out of bounds
    playerX += playerX_change

    if playerX < 0:
        playerX = 0

    if playerX > 760:
        playerX = 760

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 700:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            show_game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 770:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        for bullet in bullets:

            collision = is_collision(bullet.x, bullet.y, enemyX[i], enemyY[i])

            if collision:
                bullets.remove(bullet)
                score_value += 1
                enemyX[i] = random.randint(0, 700)
                enemyY[i] = random.randint(50, 150)

                hit_sound.play()

        enemy(enemyX[i], enemyY[i])

    for bullet in bullets:
        if bullet.y <= 0:
            bullets.remove(bullet)
            continue
        if bullet.state == 'fire':
            bullet.y += bulletY_change

        bullet.display()

    # Bullet movement
    # if bulletY <= 0:
    #     bulletY = 540
    #     bullet_state = 'ready'
    #     bullet(bulletX, bulletY)

    show_score(text_x, text_y)
    player(playerX, playerY)

    # After you define event Handlers, you update the display.
    pygame.display.update()
