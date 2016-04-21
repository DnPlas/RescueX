import pygame, sys, time
from pygame.locals import *

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

loopQuit = False
while loopQuit == False:
    outstr = ""
    for i in range(0,4):
        axis = joystick.get_axis(i)
        outstr = outstr + str(i) + ":" + str(axis) + "|"
    print(outstr)
    for event in pygame.event.get():
        if event.type == QUIT:
            loopQuit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loopQuit = True
pygame.quit()
sys.exit()
