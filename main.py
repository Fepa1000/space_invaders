"""
    This is a game that simulates the Atari classic "Space Invaders".
"""

import pygame
import random
import math

#  Initialize pygame
pygame.init()

#  Create game screen
screen = pygame.display.set_mode((800, 600))

#  Set icon, title and background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("background.jpg")

#  Player variables
img_player = pygame.image.load("x-wing.png")
player_x = 368 # 400 - 32
player_y = 536 # 600 - 64
player_x_change = 0

#  Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 5

for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("death-star.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(30, 200))
    enemy_x_change.append(0.3)
    enemy_y_change.append(3)

#  Laser variables
img_laser = pygame.image.load("laser.png")
laser_x = 0
laser_y = 536
laser_x_change = 0
laser_y_change = 0.5
laser_visible = False

#  Score variables
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

# End game
end_font = pygame.font.Font("freesansbold.ttf", 64)

# Game over message
def game_over():
    game_over_text = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 200))

# Show score
def show_score(x, y):
    text = score_font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))

# Show player on the screen
def player(x, y):
    screen.blit(img_player, (x, y))


# Show enemy on the screen
def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))


def shoot_laser(x, y):
    global laser_visible
    laser_visible = True
    screen.blit(img_laser, (x + 16, y + 10))


def detect_collision(x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if distance < 27:  # Check for collision.
        return True
    else:
        return False


#  Game Loop
is_running = True
while is_running:
    # RGB Background
    screen.blit(background, (0, 0))

    #  player_x += 0.1 (This was just a test for player movement)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            #  print("A key was pressed")
            if event.key == pygame.K_LEFT:  # If left arrow is pressed
                #  print("Left arrow pressed")
                player_x_change -= 0.3
            if event.key == pygame.K_RIGHT:  # If right arrow is pressed
                #  print("Right arrow pressed")
                player_x_change += 0.3
            if event.key == pygame.K_SPACE:
                if not laser_visible:
                    #  Or if laser_visible == False (Not as efficient)
                    laser_x = player_x
                    shoot_laser(laser_x, laser_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #  print("Arrow keys were released")
                player_x_change = 0

    #  Update player location
    player_x += player_x_change

    #  Keep player inside the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_enemies):
        #  End of game
        if enemy_y[i] > 450:
            for j in range(number_of_enemies):
                enemy_y[j] = 1000
            game_over()
            break

        #  Update enemy location
        enemy_x[i] += enemy_x_change[i]

        #  Keep enemy inside the screen
        if enemy_x[i] <= 0:
            enemy_x_change[i] += 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] -= 0.3
            enemy_y[i] += enemy_y_change[i]

        # Detect collision
        collision = detect_collision(enemy_x[i], enemy_y[i], laser_x, laser_y)
        if collision:
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(30, 200)
            laser_visible = False
            score += 1
            laser_y = 500
            # print(score)

        #  Show enemy
        enemy(enemy_x[i], enemy_y[i], i)

    #  Shoot laser
    if laser_y <= -64:
        laser_y = 500
        laser_visible = False
    if laser_visible:
        shoot_laser(laser_x, laser_y)
        laser_y -= laser_y_change

    #  Show player
    player(player_x, player_y)

    # Show score
    show_score(score_text_x, score_text_y)

    #  Update screen
    pygame.display.update()
