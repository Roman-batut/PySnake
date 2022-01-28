#Imports
import pyautogui
import time, subprocess
import ctypes, os

import pygame
from pygame import mixer
from PIL import Image, ImageFilter

#Image Match
def match(imageName) : 
    # Load Images
    image = ('date/images\\' + imageName + '.png')
    
    # Coordinates
    try :
        imageX, imageY = pyautogui.locateCenterOnScreen(image)
        return(imageX, imageY)
    except TypeError : 
        return(False)

#Image Blur
def blur(display) :
    pygame.image.save(display, "assets/paused.jpeg")
    pausedImage = Image.open("assets/paused.jpeg")
    blurredImage = pausedImage.filter(ImageFilter.GaussianBlur(3))
    blurredImage.save('assets/paused.jpeg')
    pausedImage = pygame.image.load("assets/paused.jpeg")
    display.blit(pausedImage, (0, 0))

#Image Rotation 
def rotation(image, rect, angle):
    imageRotation = pygame.transform.rotate(image, angle)
    return imageRotation

#Image Color
def changeColor(image,colorOriginal,colorReplace):
        imageReplace = pygame.PixelArray(image)
        imageReplace.replace(colorOriginal,colorReplace)
        imageFinale = imageReplace.make_surface()
        return imageFinale

#Admin Check
def admin():
    try:
        admin = (os.getuid() == 0)	# if Unis
    except AttributeError:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0	# elese if Windows
    return admin