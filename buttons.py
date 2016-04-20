import pygame as p
import sys
from time import *
from pygame.locals import *

class Buttons(object):
    def __init__(self):
        self.pgame = p.init()
        self.j_init = p.joystick.init()
        self.pgame
        self.j_init
  
        self.joystick = p.joystick.Joystick(0)
        self.joystick.init()
    def get(self):
        loopQuit = False
        while loopQuit == False:
            outstr = ""
            for i in range(0,numbuttons):
                button = joystick.get_button(i)
                outstr = outstr + str(i) + ":" + str(button) + "|"
                print(outstr)
                sleep(1)
    
            for event in pygame.event.get():
                if event.type == QUIT:
                    loopQuit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        loopQuit = True
#pygame.quit()
#sys.exit()
