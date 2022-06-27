#Ashab Naveed
#Henry Wise Wood High School
#Comp Sci 10
#Game Project
#December 23rd, 2021 - January 7th 2022

#Imports neccessary elements
import pygame
import os
import random
pygame.init()

# This is the costant screen size 
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#This portion loads up all of the assets and images required to run the game through the given file paths for each sprite, assigning them to a variable
RUNNING = [pygame.image.load(os.path.join("Assets/Player", "PlayerRun1.png")),
           pygame.image.load(os.path.join("Assets/Player", "PlayerRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Player", "PlayerJump.png"))
CROUCHING = [pygame.image.load(os.path.join("Assets/Player", "Playercrouch1.png")),
           pygame.image.load(os.path.join("Assets/Player", "Playercrouch2.png"))]



SMALL_Obstacle = [pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle1.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle2.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "SmallObstacle3.png"))]
LARGE_Obstacle = [pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle1.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle2.png")),
                pygame.image.load(os.path.join("Assets/Obstacle", "LargeObstacle3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
background = pygame.image.load(os.path.join("Assets/Other", "ground.png"))

#This creates a player class and sets the position on the map, with jump velocity and defines a Y value when Crouching
class Player_Main:
    X_POS = 80
    Y_POS = 300
    Y_POS_CROUCH = 310
    JUMP_VEL = 8
#Loads the images and initializes the player.
    def __init__(player):
        player.CROUCH_img = CROUCHING
        player.run_img = RUNNING
        player.jump_img = JUMPING
#creates 3 variables with one constantly being True until a keystroke is entered, thus making the other two False until a user input is given
        player.Player_CROUCH = False
        player.Player_run = True
        player.Player_jump = False

        player.step_index = 0
        player.jump_vel = player.JUMP_VEL
        player.image = player.run_img[0]
        player.Player_rect = player.image.get_rect()
        player.Player_rect.x = player.X_POS
        player.Player_rect.y = player.Y_POS
#When a user inputs a keystroke, the player will jump or CROUCH, or else the player continues running through the course
    def update(player, userInput):
        if player.Player_CROUCH:
            player.CROUCH()
        if player.Player_run:
            player.run()
        if player.Player_jump:
            player.jump()

        if player.step_index >= 10:
            player.step_index = 0
#Takes user inputs in order to allow controls
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE] or userInput[pygame.K_w]) and not player.Player_jump:
            player.Player_CROUCH = False
            player.Player_run = False
            player.Player_jump = True
        elif (userInput[pygame.K_DOWN] or userInput [pygame.K_s]) and not player.Player_jump:
            player.Player_CROUCH = True
            player.Player_run = False
            player.Player_jump = False
        elif not (player.Player_jump or userInput[pygame.K_DOWN]):
            player.Player_CROUCH = False
            player.Player_run = True
            player.Player_jump = False
#Creates the crouching mechanic using the sprite changing the Y value (Lower)
    def CROUCH(player):
        player.image = player.CROUCH_img[player.step_index // 5]
        player.Player_rect = player.image.get_rect()
        player.Player_rect.x = player.X_POS
        player.Player_rect.y = player.Y_POS_CROUCH
        player.step_index += 1
#Creates the running mechanic using the sprites changing the X value
    def run(player):
        player.image = player.run_img[player.step_index // 5]
        player.Player_rect = player.image.get_rect()
        player.Player_rect.x = player.X_POS
        player.Player_rect.y = player.Y_POS
        player.step_index += 1
#Creates the jumping mechanic using the sprites and changing the Y value (Higher), with a jump velocity
    def jump(player):
        player.image = player.jump_img
        if player.Player_jump:
            player.Player_rect.y -= player.jump_vel * 4
            player.jump_vel -= 0.8
        if player.jump_vel < - player.JUMP_VEL:
            player.Player_jump = False
            player.jump_vel = player.JUMP_VEL
#Adds the player to the screen
    def draw(player, SCREEN):
        SCREEN.blit(player.image, (player.Player_rect.x, player.Player_rect.y))

#Randomly adds clouds around the course
class Cloud:
    def __init__(player):
        player.x = SCREEN_WIDTH + random.randint(800, 1000)
        player.y = random.randint(50, 100)
        player.image = CLOUD
        player.width = player.image.get_width()
#Adds game speed
    def update(player):
        player.x -= game_speed
        if player.x < -player.width:
            player.x = SCREEN_WIDTH + random.randint(2500, 3000)
            player.y = random.randint(50, 100)

    def draw(player, SCREEN):
        SCREEN.blit(player.image, (player.x, player.y))

#Creates a class for the player as an obstacle, allowing collision
class Obstacle:
    def __init__(player, image, type):
        player.image = image
        player.type = type
        player.rect = player.image[player.type].get_rect()
        player.rect.x = SCREEN_WIDTH

    def update(player):
        player.rect.x -= game_speed
        if player.rect.x < -player.rect.width:
            obstacles.pop()

    def draw(player, SCREEN):
        SCREEN.blit(player.image[player.type], player.rect)

#Small obstacle and sets the y position
class SmallObstacle(Obstacle):
    def __init__(player, image):
        player.type = random.randint(0, 2)
        super().__init__(image, player.type)
        player.rect.y = 310

#Large Obstacles
class LargeObstacle(Obstacle):
    def __init__(player, image):
        player.type = random.randint(0, 2)
        super().__init__(image, player.type)
        player.rect.y = 290

#Creates a class of a "Bird" which becomes another obstacle with a unique y value.
class Bird(Obstacle):
    def __init__(player, image):
        player.type = 0
        super().__init__(image, player.type)
        player.rect.y = 240
        player.index = 0

    def draw(player, SCREEN):
        if player.index >= 9:
            player.index = 0
        SCREEN.blit(player.image[player.index//5], player.rect)
        player.index += 1

#sets the main game space 
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Player_Main()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
#Adds the score variable and creates a multiplier for the longer the game runs
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
#Displays the points
        text = font.render("Points: " + str(points), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)
#Creates a background
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed



    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
#Fills the screen and creates the loading screen
        SCREEN.fill((16, 201, 224))


        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallObstacle(SMALL_Obstacle))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeObstacle(LARGE_Obstacle))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
#Collision detection
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.Player_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
#Creates the coloured background for the starting screen
    while run:
        SCREEN.fill((204, 204, 255))
        font = pygame.font.Font('text.ttf', 15) #loads up the .ttf file in order to use the font
#Adds text with the defined font and size
        if death_count == 0: #the main menu that loads up if the user has just started playing
            text = font.render("Press any Key to Start", True, (255, 255, 255))
            SCREEN.blit(background, (0,0))
        
        elif death_count > 0: #the menu that loads up after the player loses a round of the game; this is shown from this point on until the code is restarted
            text = font.render("Press any Key to Restart", True, (255, 255, 255))
            score = font.render("Your Score: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
              
            if event.type == pygame.KEYDOWN:
                main()

#sets the death count to 0 to ensure the initial loading screen launches with no errors, once this value reaches 1, it shows the restarting screen.
menu(death_count=0)



