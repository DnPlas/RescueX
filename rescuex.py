#!/usr/bin/env python

''' 
rescuex.py

This code is intended to control a rescue robot which main task is 
to rescue a person in three different scenarios:
 - A muddy inclined plane 
 - An obscure laberynth 
 - A high alttitude challenge

All tasks were tested and exectuted using a Raspberry Pi 3 B running Debian 8.

Bill of materials:

Servos 180                |  3
Continous servos          |  1
DC motors                 |  4
Webcamera                 |  1
Playstation 3 controller  |  1

Daniela A. Plascencia <daplascen@gmail.com>'''

#-----LIBRARIES-----
import pygame             #Among other options, it fetches information from the PS controller
import time               #Module of time to make delays
import RPi.GPIO as GPIO   #Gets all functionallity from RPi's GPIOs

#-----INITIAL SETUP-----
GPIO.setmode(GPIO.BOARD)  #Sets a mode so you can use the number of a pin in Raspberry Pi board
pygame.init()             
j = pygame.joystick.Joystick(0)
j.init()
print 'Welcome to RescueX. Initialized Joystick : %s' % j.get_name()

#-----ASSIGNING VARIABLES-----
MotorA0 = 16 
MotorA1 = 18
MotorAE = 22

MotorB0 = 29
MotorB1 = 31
MotorBE = 19

Servo1 = 12
Servo2 = 10
Servo3 = 8
Servo4 = 36
 
value = 0
max_val = 8
min_val = 3 

A0 = False
A1 = False
B0 = False
B1 = False

threshold = 0.60
LeftTrack = 0
RightTrack = 0
x = 0
y = 0

#-----SETTING GPIOS DIRECTION-----
GPIO.setup(MotorA0,GPIO.OUT)
GPIO.setup(MotorA1,GPIO.OUT)
GPIO.setup(MotorAE,GPIO.OUT)

GPIO.setup(MotorB0,GPIO.OUT)
GPIO.setup(MotorB1,GPIO.OUT)
GPIO.setup(MotorBE,GPIO.OUT)

GPIO.setup(Servo1, GPIO.OUT)
GPIO.setup(Servo2, GPIO.OUT)
GPIO.setup(Servo3, GPIO.OUT)
GPIO.setup(Servo4, GPIO.OUT)

#-----PWM SETUP-----
S1 = GPIO.PWM(Servo1, 50)
S2 = GPIO.PWM(Servo2, 50)
S3 = GPIO.PWM(Servo3, 50)
S4 = GPIO.PWM(Servo4, 50)

#-----GPIOS OFF-----
GPIO.output(MotorA0, A0)
GPIO.output(MotorA1, A1)
GPIO.output(MotorAE, False)
GPIO.output(MotorBE, False)
GPIO.output(MotorB0, B0)
GPIO.output(MotorB1, B1)
S1.start(min_val)
S2.start(min_val)
S3.start(min_val)
S4.start(0)

#This function gives a value to the GPIO which will control the motors
def setmotors():
        GPIO.output(MotorA0, A0)
        GPIO.output(MotorA1, A1)
        GPIO.output(MotorAE, True)
        GPIO.output(MotorBE, True)
        GPIO.output(MotorB0, B0)
        GPIO.output(MotorB1, B1)

try:
    # Turn on the motors
    GPIO.output(MotorAE, True)
    GPIO.output(MotorBE, True)

#-----MAIN LOOP-----
    while True:

        events = pygame.event.get() #Read a list of events the Playstation 3 controller makes 
        for event in events:
            UpdateMotors = 0
            
            #JOYSTICK1 & JOYSTICK2: Gets the value of joystick 1 and 2 from the Playstation 3 controller
            if event.type == pygame.JOYAXISMOTION: 
                if event.axis == 1:
                    LeftTrack = event.value
                    UpdateMotors = 1
                elif event.axis == 3:
                    RightTrack = event.value
                    UpdateMotors = 1
          
            #L1 & L2: Gets the value of triggers L1 and R1 from the Playstation 3 controller
            if event.type == pygame.JOYBUTTONDOWN: 
                if event.button == 11:
                    x = 11
                    UpdateMotors = 1
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 11:
                    x = 0
                    UpdateMotors = 1
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 10:
                    x = 10
                    UpdateMotors = 1
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 10:
                    x = 0
                    UpdateMotors = 1

            #TRIANGLE: Gets the state of button 
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 12:
                    y = 12
                    UpdateMotors = 1

            #CIRCLE: Gets the state of button 
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 13:
                    y = 13
                    UpdateMotors = 1

            #X: Gets the state of button 
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 14:
                    y = 14
                    UpdateMotors = 1
            #SQUARE: Gets the state of button
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 15:
                    y = 15
                    UpdateMotors = 1

            if UpdateMotors:

              if (y==12):
                  if (j.get_button(11) and value < max_val):
                      value = value + 0.5 
                      S1.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S1.ChangeDutyCycle(value)
 
              if (y==13):
                  if (j.get_button(11) and value < max_val):
                      value = value + 0.5
                      S2.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S2.ChangeDutyCycle(value)

              if (y==14):
                  if (j.get_button(11) and value < max_val):
                      value = value + 0.5
                      S3.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S3.ChangeDutyCycle(value)

              if (y==15):
                  if (j.get_button(11)):
                      S4.ChangeDutyCycle(5)
                  elif (j.get_button(10)):
                      S4.ChangeDutyCycle(10) 
                  else: 
                      S4.ChangeDutyCycle(0)

              # Move forwards
              if (RightTrack > threshold):
                  A0 = False
                  A1 = True 
              # Move backwards
              elif (RightTrack < -threshold):
                  A0 = True
                  A1 = False
              # Stopping
              else:
                  A0 = False
                  A1 = False

              if (LeftTrack > threshold):
                  B0 = False
                  B1 = True
              # Move backwards
              elif (LeftTrack < -threshold):
                  B0 = True
                  B1 = False
              # Otherwise stop
              else:
                  B0 = False
                  B1 = False

              setmotors()

#The script can be exited from
except KeyboardInterrupt:
    # Turn off the motors
    GPIO.output(MotorAE, False)
    GPIO.output(MotorBE, False)
    j.quit()#!/usr/bin/env python

GPIO.cleanup()
