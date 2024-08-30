import pygame
import time
import random

pygame.init()

# R,G,B - SomeColors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (17, 124, 47)
blue = (0, 0, 255)

#LoadingImages
sunImg = pygame.image.load("images/bgSunset1.png")
bgImg = pygame.image.load("images/MAP01.png")

netImg = pygame.image.load("images/net01.png")
monImg = pygame.image.load("images/mon01.png")
mon2Img = pygame.image.load("images/mon02.png")
mon3Img = pygame.image.load("images/mon03.png")
bombImg = pygame.image.load("images/bomb.png")

startImg = pygame.image.load("images/starticon.png")
quitImg = pygame.image.load("images/quiticon.png")

clickStartImg = pygame.image.load("images/clickedStartIcon.png")
clickQuitImg = pygame.image.load("images/clickedQuitIcon.png")


#SettingFrame
display_width = 550
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Cricker Game")

#SettingClock
clock = pygame.time.Clock()

#PlayerClassParameters
netparms = [netImg, 5, 200, 450, 30, 30, 1.1]

#ButtonClass
class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            gameDisplay.blit(img_act,(x_act, y_act))
            if click[0] and action != None:
                time.sleep(2)
                action()
        else:
            gameDisplay.blit(img_in,(x,y))

# BackgroundClass
class Background:
    def __init__(self, bg_img, bg_x, bg_y):
        self.bg_x = bg_x
        self.bg_y = bg_y
        gameDisplay.blit(bg_img, (bg_x, bg_y))

# PlayerClass
class Player:
    def __init__(self,p_img,speedIn,net_x,net_y,hitbox_x,hitbox_y,speedmultiplier):
        self.speed = speedIn
        self.net_x = net_x
        self.net_y = net_y
        self.p_img = p_img
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y
        self.speedmult = speedmultiplier


# GameObjectsClass
class Gameobject:
    def __init__(self, b_image, speed, coord_x, coord_y, hitbox_x, hitbox_y):
        self.b_image = b_image
        self.speed = speed
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y

# ScoreFunction
def scorecounter(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score:" + str(count), True, black)
    gameDisplay.blit(text, (0, 0))

# CrashFunction/MessageDisplay
def text_objects(text, font):
    textsurface = font.render(text, True, black)
    return textsurface, textsurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf", 46)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def crash(message):
    message_display(message)

#QuitFunction
def quitgame():
    pygame.quit()
    quit()

#MainMenu
def mainmenu():

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        #titletext = gameDisplay.blit(titleImg, (275,200))
        bg = Background(sunImg, 0, 0)
        startButton = Button(startImg,150,260,60,20,clickStartImg,150,260,game_loop)
        quitButton = Button(quitImg,330,260,60,20,clickQuitImg,330,260,quitgame)

        pygame.display.update()
        clock.tick(15)

#MainGame
def game_loop():

#CreatingObjects
    net = Player(netparms[0],netparms[1],netparms[2],netparms[3],netparms[4],netparms[5],netparms[6])
    mon = Gameobject(monImg, random.randint(3,5), random.randrange(0, display_width - 20),-600,40,35)
    mon2 = Gameobject(mon2Img,random.randint(5,7), random.randrange(0, display_width - 20),-600,40,35)
    mon3 = Gameobject(mon3Img,random.randint(5,7), random.randrange(0, display_width - 20),-600,40,35)
    bomb = Gameobject(bombImg, 1, random.randrange(0, display_width - 20),-600,40,35)

#Constants
    x_change = 0
    score = 0

    gameexit = False
#GameLoop
    while not gameexit:

#Background
        gameDisplay.fill(white)
        bg = Background(bgImg, 0, 0)
# Objects
        #Monster Object
        gameDisplay.blit(mon.b_image, (mon.coord_x, mon.coord_y))
        gameDisplay.blit(mon2.b_image, (mon2.coord_x, mon2.coord_y))
        gameDisplay.blit(mon3.b_image, (mon3.coord_x, mon3.coord_y))
        #Bomb Object
        gameDisplay.blit(bomb.b_image, (bomb.coord_x, bomb.coord_y))

#Player
        gameDisplay.blit(net.p_img, (net.net_x,net.net_y))

#Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and net.net_x > 0:
                    x_change = net.speed*-1 + -1*net.speedmult*score
                elif event.key == pygame.K_RIGHT and net.net_x < display_width - 45:
                    x_change = net.speed + net.speedmult*score
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        net.net_x += x_change

# ObjectSpeeds
        mon.coord_y += mon.speed
        mon2.coord_y += mon.speed
        mon3.coord_y += mon.speed
        bomb.coord_y += bomb.speed + 1.1 * score

# Boundaries
        if net.net_x > display_width - net.hitbox_x or net.net_x < 0:
            x_change = 0

# ReObjects
        if mon.coord_y > display_height:
            mon.coord_y = -10
            mon.coord_x = random.randrange(0, display_width - 25)
        if mon2.coord_y > display_height:
            mon2.coord_y = -10
            mon2.coord_x = random.randrange(0, display_width - 25)
        if mon3.coord_y > display_height:
            mon3.coord_y = -10
            mon3.coord_x = random.randrange(0, display_width - 25)
        if bomb.coord_y > display_height - 10:
            bomb.coord_y = -10
            bomb.coord_x = random.randrange(0, display_width - 25)
# Score
        scorecounter(score)

# เงื่อนไข
    # Bomb
        if net.net_y < bomb.coord_y + bomb.hitbox_y and net.net_y > bomb.coord_y or net.net_y + net.hitbox_y > bomb.coord_y and net.net_y + net.hitbox_y < bomb.coord_y + bomb.hitbox_y:
            if net.net_x > bomb.coord_x and net.net_x < bomb.coord_x + bomb.hitbox_x or net.net_x + net.hitbox_x > bomb.coord_x and net.net_x + net.hitbox_x < bomb.coord_x + bomb.hitbox_x:
                crash("Oh no! You got a bomb!")

    # Monster
        if net.net_y < mon.coord_y + mon.hitbox_y and net.net_y > mon.coord_y or net.net_y + net.hitbox_y > mon.coord_y and net.net_y + net.hitbox_y < mon.coord_y + mon.hitbox_y:
            if net.net_x > mon.coord_x and net.net_x < mon.coord_x + mon.hitbox_x or net.net_x + net.hitbox_x > mon.coord_x and net.net_x + net.hitbox_x < mon.coord_x + mon.hitbox_x:
                mon.coord_y = -10
                mon.coord_x = random.randrange(0, display_width - 25)
                score += 1
                print(score)
        if net.net_y < mon2.coord_y + mon2.hitbox_y and net.net_y > mon2.coord_y or net.net_y + net.hitbox_y > mon2.coord_y and net.net_y + net.hitbox_y < mon2.coord_y + mon2.hitbox_y:
            if net.net_x > mon2.coord_x and net.net_x < mon2.coord_x + mon2.hitbox_x or net.net_x + net.hitbox_x > mon2.coord_x and net.net_x + net.hitbox_x < mon2.coord_x + mon2.hitbox_x:
                mon2.coord_y = -10
                mon2.coord_x = random.randrange(0, display_width - 25)
                score += 2
                print(score)
        if net.net_y < mon3.coord_y + mon3.hitbox_y and net.net_y > mon3.coord_y or net.net_y + net.hitbox_y > mon3.coord_y and net.net_y + net.hitbox_y < mon3.coord_y + mon3.hitbox_y:
            if net.net_x > mon3.coord_x and net.net_x < mon3.coord_x + mon3.hitbox_x or net.net_x + net.hitbox_x > mon3.coord_x and net.net_x + net.hitbox_x < mon3.coord_x + mon3.hitbox_x:
                mon3.coord_y = -10
                mon3.coord_x = random.randrange(0, display_width - 25)
                score -= 1
                print(score)

        pygame.display.update()
        clock.tick(60)

mainmenu()
game_loop()
pygame.QUIT()
quit()