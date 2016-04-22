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
MotorA0 = 16 #H-Bridge inputs for the left pair of motors
MotorA1 = 18

MotorB0 = 29 #H-Bridge inputs for the right pair of motors
MotorB1 = 31

Servo1 = 12 #Clamp servo
Servo2 = 10 #Rack gear clamp
Servo3 = 8 #Positioning clamp servo
Servo4 = 36 #Lifting crane servo
 
value = 0 #Control variable
max_val = 8 #This is the maximum duty cycle for every servo
min_val = 3 #Minimim duty cycle for every servo

A0 = False #Initialise variable in 0
A1 = False #Initialise variable in 0
B0 = False #Initialise variable in 0
B1 = False #Initialise variable in 0

threshold = 0.60 #Control variable. Pygame takes the value of a joystick and compares it to a treshold so it can establish a set of values where the joystick will be detected as up or down movement
LeftTrack = 0 #Control variables: flags that permit access to an specific function
RightTrack = 0
x = 0
y = 0

#-----SETTING GPIOS DIRECTION-----
GPIO.setup(MotorA0,GPIO.OUT) #Sets GPIOs as outputs
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
S1 = GPIO.PWM(Servo1, 50) #Establishes an assignment to a variable with the module PWM (set), number of pin (ServoX) and frequency (50 Hz)
S2 = GPIO.PWM(Servo2, 50)
S3 = GPIO.PWM(Servo3, 50)
S4 = GPIO.PWM(Servo4, 50)

#-----GPIOS OFF-----
GPIO.output(MotorA0, A0) #Start all GPIOs in zero so they do not move during the processing
GPIO.output(MotorA1, A1)
GPIO.output(MotorAE, False)
GPIO.output(MotorBE, False)
GPIO.output(MotorB0, B0)
GPIO.output(MotorB1, B1)
S1.start(min_val) #Starts servos at their minimum duty cycle
S2.start(min_val)
S3.start(min_val)
S4.start(0)

#This function gives a value to a certain GPIO, then it sends it to an H-bridge so a combination of digital values are written in the H-bride.
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
          
            #L1 & L2: Gets the value of triggers R1 from the Playstation 3 controller
            if event.type == pygame.JOYBUTTONDOWN: 
                if event.button == 11:
                    x = 11
                    UpdateMotors = 1
            elif event.type == pygame.JOYBUTTONUP:
                if event.button == 11:
                    x = 0
                    UpdateMotors = 1
            
            #L1 & L2: Gets the value of triggers L1 from the Playstation 3 controller
            
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

            #Main loop. Depending on the pressed button, Raspberry Pi will send a digital output to any of the specified GPIO
            if UpdateMotors:
            
              if (y==12): #When triangle is pressed, you can move a servo (S1) to rotate clockwise (R1) or counter clockwise(L1)
                  if (j.get_button(11) and value < max_val):
                      value = value + 0.5 
                      S1.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S1.ChangeDutyCycle(value)
 
              if (y==13): #When circle is pressed, you can move a servo (S2) to to rotate clockwise (R1) or counter clockwise(L1)
                  if (j.get_button(11) and value < max_val):
                      value = value + 0.5
                      S2.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S2.ChangeDutyCycle(value)

              if (y==14): #When x is pressed, you can move a servo (S3) to rotate clockwise (R1) or counter clockwise(L1)
o                 if (j.get_button(11) and value < max_val):
                      value = value + 0.5
                      S3.ChangeDutyCycle(value)
                  elif (j.get_button(10) and value > min_val):
                      value = value - 0.5
                      S3.ChangeDutyCycle(value)

              if (y==15): #When square is pressed, you can move a servo (S4) to rotate clockwise (R1) or counter clockwise (L1)
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
