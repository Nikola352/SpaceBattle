### SPACE BATTLE ###
# created by Nikola
import pygame, time, sys, random, os
from pygame.locals import *

# The player
class Player(pygame.Rect):
    def __init__(self):
        super(Player, self).__init__(WINDOW_WIDTH/2-85, 0.8*WINDOW_HEIGHT, 60,50)
        image = pygame.image.load('images\\player.png')
        self.image = pygame.transform.scale(image,(60,50))
        windowSurface.blit(self.image, self)
        self.health = 3

    def moveLeft(self):
        if player.left - PLAYER_SPEED > 0:
            self.left -= PLAYER_SPEED

    def moveRight(self):
        if player.right + PLAYER_SPEED < WINDOW_WIDTH:
            self.right += PLAYER_SPEED

    def shoot(self):
        missiles.append(Missile(self.centerx-10, self.top))

# Player fires the missiles
class Missile(pygame.Rect):
    def __init__(self, x, y):
        super(Missile, self).__init__(x,y,20,40)
        image = pygame.image.load('images\\missile.png')
        self.image = pygame.transform.scale(image,(20,40))  #20,40
        windowSurface.blit(self.image, self)

# Alien class
class Alien(pygame.Rect):
    def __init__(self, color, x):
        super(Alien, self).__init__(x,0,85,50)
        image = pygame.image.load('images\\alien_'+color+'.png')
        self.image = pygame.transform.scale(image,(85,50))
        windowSurface.blit(self.image, self)
        self.timeToDrop = 0
        self.color = color
        if self.color == 'yellow':
            self.health = 3
            self.bombRate = 60  # Time between bomb drops: (bombRate / FPS) seconds
        else:
            self.health = 5
            self.bombRate = 40

    def dropBomb(self):
        bombs.append(Bomb(self.centerx-15,self.bottom))

# Aliens drop bombs
class Bomb(pygame.Rect):
    def __init__(self,x,y):
        super(Bomb, self).__init__(x,y,30,40)
        image = pygame.image.load('images\\bomb.png')
        self.image = pygame.transform.scale(image,(30,30))
        windowSurface.blit(self.image, self)

# HelpBox is a falling object which awards when collected
class HelpBox(pygame.Rect):
    def __init__(self, x):
        super(HelpBox, self).__init__(x,0,40,80)
        image = pygame.image.load('images\\help_box.png')
        self.image = pygame.transform.scale(image, (40,80))
        self.action = random.choice([self.health, self.speed, self.slowAliens, self.bombSpeed])

    def health(self):
        global player
        player.health = 3
        return 'Full Health'

    def speed(self):
        global PLAYER_SPEED
        PLAYER_SPEED += 2
        return 'Extra speed'

    def slowAliens(self):
        global ALIEN_SPEED
        if ALIEN_SPEED > 1:
            ALIEN_SPEED -= 1
            return 'Slowing the aliens down'
        else:
            return "Aliens can't be slower"

    def bombSpeed(self):
        global BOMB_SPEED
        if BOMB_SPEED > ALIEN_SPEED + 1:
            BOMB_SPEED -= 2
            return 'Bombs falling slower'
        else:
            return "Bombs can't fall slower"


def drawText(surface,text,font,x,y):
    # Function for writting text to the screen
    textobj = font.render(text, 1, YELLOW)
    textRect = textobj.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textobj,textRect)

def drawScreen(backgroundImg, bgRect, player, aliens, missiles, bombs):
    # Draws everything to the screen, except helpBoxes
    windowSurface.blit(backgroundImg, bgRect)

    windowSurface.blit(player.image, player)

    for alien in aliens:
        windowSurface.blit(alien.image, alien)

    for missile in missiles[:]:
        windowSurface.blit(missile.image, missile)

    for bomb in bombs[:]:
        windowSurface.blit(bomb.image, bomb)

    if player.health > 0:
        windowSurface.blit(heart, (10, 0.93*WINDOW_HEIGHT, 30, 30))
    if player.health > 1:
        windowSurface.blit(heart, (50, 0.93*WINDOW_HEIGHT, 30, 30))
    if player.health > 2:
        windowSurface.blit(heart, (90, 0.93*WINDOW_HEIGHT, 30, 30))

    drawText(windowSurface, f'Score: {SCORE}', font, 0.7*WINDOW_WIDTH, 0.9*WINDOW_HEIGHT)


# CONSTANT VARIABLES
FPS = 30             # Frames Per Second
PLAYER_SPEED = 10    # number of pixels that player moves on1 key press
ALIEN_SPEED = 4
MISSILE_SPEED = 10   # speed of a missile fired by player
BOMB_SPEED = 15       # speed of an alien's bomb
NEW_ALIEN_RATE = 60  # time which takes new alien to spawn = FPS / NEW_ALIEN_RATE
INCREASE_ALIEN_RATE = 150
HELPBOX_RATE = 400
BOX_SPEED = 5
YELLOW = (255,255,0)

#Initialise pygame
pygame.init()
mainClock = pygame.time.Clock()

#Set up the window
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)
pygame.display.set_caption('Space Battle')

# Fonts
font = pygame.font.SysFont('Arial', 50)
fontBig = pygame.font.SysFont('Arial', 80, bold=True)
fontSmall = pygame.font.SysFont('Arial', 20, bold=True)
fontHB = pygame.font.SysFont('Arial', 30, italic=True)

# Sounds
bombSound = pygame.mixer.Sound('sounds\\Bomb-Sound.wav')
missileSound = pygame.mixer.Sound('sounds\\Grenade-Sound.wav')
launchSound = pygame.mixer.Sound('sounds\\flyby-Conor.wav')
pygame.mixer.music.load('sounds\\Car-Theft-101.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# Heart image
img = pygame.image.load('images\\heart-th.png')
heart = pygame.transform.scale(img,(30,30))

# The background image
bgimg = pygame.image.load('images\\background.png')
backgroundImg = pygame.transform.scale(bgimg,(WINDOW_WIDTH,WINDOW_HEIGHT))
bgRect = pygame.Rect(0,0,WINDOW_WIDTH,WINDOW_HEIGHT)

#START SCREEN
windowSurface.blit(backgroundImg, bgRect)
drawText(windowSurface, 'SPACE BATTLE', fontBig, 0.25*WINDOW_WIDTH, 0.25*WINDOW_HEIGHT)
drawText(windowSurface, 'PLAY', font, 0.3*WINDOW_WIDTH, 0.45*WINDOW_HEIGHT)
pygame.draw.rect(windowSurface, YELLOW, (0.29*WINDOW_WIDTH, 0.445*WINDOW_HEIGHT,120,65), 5)
drawText(windowSurface, 'How to Play', font, 0.5*WINDOW_WIDTH, 0.45*WINDOW_HEIGHT)
pygame.draw.rect(windowSurface, YELLOW, (0.495*WINDOW_WIDTH, 0.445*WINDOW_HEIGHT,230,65), 5)

drawText(windowSurface, 'created by Nikola', fontSmall, 0.8*WINDOW_WIDTH, 0.9*WINDOW_HEIGHT)

pygame.display.update()

next = False
showHelp = False
while not next:  ### THE START SCREEN
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            if event.pos[0] > 0.29*WINDOW_WIDTH and event.pos[0] < 0.29*WINDOW_WIDTH+120:
                if event.pos[1] > 0.445*WINDOW_HEIGHT and event.pos[1] < 0.445*WINDOW_HEIGHT+65:
                    next = True
            if event.pos[0] > 0.49*WINDOW_WIDTH and event.pos[0] < 0.49*WINDOW_WIDTH+230:
                if event.pos[1] > 0.445*WINDOW_HEIGHT and event.pos[1] < 0.445*WINDOW_HEIGHT+65:
                    showHelp = True

    if showHelp: # 'How to play' screen
        windowSurface.blit(backgroundImg, bgRect)
        drawText(windowSurface, 'HOW TO PLAY', fontBig, 0.26*WINDOW_WIDTH, 0.2*WINDOW_HEIGHT)
        line = []
        line.append('You are the blue spaceship in the bottom of the screen. Use arrow keys to move.')
        line.append('Aliens are constantly coming from above to attack you! Avoid them and their bombs. ')
        line.append('Each time you get hit you lose a life (heart in the bottom left corner). You can')
        line.append('shoot missiles on aliens by pressing the SPACE key. It takes 5 hits to destroy a red')
        line.append('alien, and 3 to destroy a yellow one. Destroy as many of them as you can to increase')
        line.append('your score (bottom right corner). Enjoy!')
        for i in range(0,len(line)):
            drawText(windowSurface, line[i], fontSmall, 0.16*WINDOW_WIDTH, (0.4+i*0.05)*WINDOW_HEIGHT)

        drawText(windowSurface, 'PLAY', font, 0.45*WINDOW_WIDTH, 0.75*WINDOW_HEIGHT)
        pygame.draw.rect(windowSurface, YELLOW, (0.44*WINDOW_WIDTH, 0.745*WINDOW_HEIGHT,120,65), 5)

        drawText(windowSurface, 'created by Nikola', fontSmall, 0.8*WINDOW_WIDTH, 0.9*WINDOW_HEIGHT)

        pygame.display.update()

        while not next:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    if event.pos[0] > 0.44*WINDOW_WIDTH and event.pos[0] < 0.44*WINDOW_WIDTH+120:
                        if event.pos[1] > 0.745*WINDOW_HEIGHT and event.pos[1] < 0.745*WINDOW_HEIGHT+65:
                            next = True


# Background music
pygame.mixer.music.load('sounds\\Deep_Space_Destructors_-_04_-_From_The_Ashes.mp3')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
### START OF THE GAME
while True:
    # Set up data structures
    aliens = []
    missiles = []
    bombs = []

    addAlien = 0 # variable for controlling aliens spawnspeed
    addHelpBox = 0
    increaseRate = 0

    player = Player() # The player

    # Movement variables
    moveLeft = False
    moveRight = False

    SCORE = 0

    # The game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_SPACE:
                    player.shoot()
                    launchSound.play()

            if event.type == KEYUP:
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False


        # Move the player
        if moveLeft:
            player.moveLeft()
        if moveRight:
            player.moveRight()

        if increaseRate == INCREASE_ALIEN_RATE:
            increaseRate = 0
            NEW_ALIEN_RATE -= 1


        # Help boxes
        addHelpBox += 1
        if addHelpBox == HELPBOX_RATE:
            addHelpBox = 0
            x = random.randint(0,WINDOW_WIDTH-40)
            helpBox = HelpBox(x)
        try:
            helpBox.top += BOX_SPEED
            if helpBox.colliderect(player):
                message = helpBox.action()
                drawScreen(backgroundImg, bgRect, player, aliens, missiles, bombs)
                drawText(windowSurface, message, fontHB, 0.3*WINDOW_WIDTH, 0.9*WINDOW_HEIGHT)
                pygame.display.update()
                pygame.time.wait(800)
                del helpBox
            if helpBox.bottom > 0.85 * WINDOW_HEIGHT:
                del helpBox
        except NameError:
            pass


        addAlien += 1  # When 'addAlien' reaches the NEW_ALIEN_RATE, spawn a new alien
        if addAlien == NEW_ALIEN_RATE:
            addAlien = 0
            x = random.randint(0, WINDOW_WIDTH-85)
            color = random.choice(['yellow', 'yellow', 'red'])
            alien = Alien(color, x)
            alien.dropBomb()
            aliens.append(alien)

        for alien in aliens:
            alien.top += ALIEN_SPEED
            if alien.colliderect(player):
                bombSound.play()
                player.health -= 1
                aliens.remove(alien)
            if alien.bottom >= 0.85 * WINDOW_HEIGHT:
                aliens.remove(alien)
            alien.timeToDrop += 1
            if alien.timeToDrop == alien.bombRate:
                alien.timeToDrop = 0
                alien.dropBomb()

        # Handle bombs and missiles
        for missile in missiles[:]:
            if missile.bottom < 0:
                missiles.remove(missile)
            else:
                missile.top -= MISSILE_SPEED
                for alien in aliens:  # For each alien
                    if missile.colliderect(alien):  # If the bomb has hit an alien
                        try:
                            missiles.remove(missile)
                            missileSound.play()
                            alien.health -= 1
                            if alien.health == 0:  # If the alien's health is zero, he dies
                                aliens.remove(alien)
                                if alien.color == 'yellow':
                                    SCORE += 30
                                else:
                                    SCORE += 50
                        except ValueError:
                            pass

        for bomb in bombs[:]:
            if bomb.bottom > 0.85*WINDOW_HEIGHT:
                bombs.remove(bomb)
            else:
                bomb.top += BOMB_SPEED
                if bomb.colliderect(player):
                    bombSound.play()
                    bombs.remove(bomb)
                    player.health -= 1

        # Draw everything onto the window surface
        drawScreen(backgroundImg, bgRect, player, aliens, missiles, bombs)
        try:
            windowSurface.blit(helpBox.image, helpBox)
        except NameError:
            pass
        pygame.display.update()

        if player.health == 0: # When the player loses, go to game over screen
            break

        mainClock.tick(FPS)

    windowSurface.blit(backgroundImg, bgRect)
    drawText(windowSurface, 'GAME OVER', fontBig, 0.28*WINDOW_WIDTH, 0.3*WINDOW_HEIGHT)
    drawText(windowSurface, 'Play Again', font, 0.4*WINDOW_WIDTH, 0.5*WINDOW_HEIGHT)
    pygame.draw.rect(windowSurface, YELLOW, (0.39*WINDOW_WIDTH, 0.495*WINDOW_HEIGHT,210,70), 5)
    drawText(windowSurface, f'Score: {SCORE}', font, 0.7*WINDOW_WIDTH, 0.9*WINDOW_HEIGHT)


    pygame.display.update()

    next = False
    while not next:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if event.pos[0] > 0.39*WINDOW_WIDTH and event.pos[0] < 0.39*WINDOW_WIDTH+210:
                    if event.pos[1] > 0.495*WINDOW_HEIGHT and event.pos[1] < 0.495*WINDOW_HEIGHT+70:
                        next = True

    # Reset the global variables
    NEW_ALIEN_RATE = 60
    PLAYER_SPEED = 10
    ALIEN_SPEED = 4
    BOMB_SPEED = 15
