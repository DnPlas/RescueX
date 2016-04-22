#!/usr/bin/env python

import pygame
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# Initialise the pygame library
pygame.init()

# Connect to the first JoyStick
j = pygame.joystick.Joystick(0)
j.init()

print 'Initialized Joystick : %s' % j.get_name()

# Setup the various GPIO values, using the BCM numbers for now
MotorA0 = 16
MotorA1 = 18
MotorAE = 22

MotorB0 = 23
MotorB1 = 21
MotorBE = 19

Servo1 = 12
Servo2 = 10
Servo3 = 8

value = 0
max_val = 11.5
min_val = 2 

A0 = False
A1 = False
B0 = False
B1 = False



GPIO.setup(MotorA0,GPIO.OUT)
GPIO.setup(MotorA1,GPIO.OUT)
GPIO.setup(MotorAE,GPIO.OUT)

GPIO.setup(MotorB0,GPIO.OUT)
GPIO.setup(MotorB1,GPIO.OUT)
GPIO.setup(MotorBE,GPIO.OUT)

GPIO.setup(Servo1, GPIO.OUT)
GPIO.setup(Servo2, GPIO.OUT)
GPIO.setup(Servo3, GPIO.OUT)

S1 = GPIO.PWM(Servo1, 50)
S2 = GPIO.PWM(Servo2, 50)
S3 = GPIO.PWM(Servo3, 50)

# Set all the Motors to 'off'
GPIO.output(MotorA0, A0)
GPIO.output(MotorA1, A1)
GPIO.output(MotorAE, False)
GPIO.output(MotorBE, False)
GPIO.output(MotorB0, B0)
GPIO.output(MotorB1, B1)
S1.start(2)
S2.start(0)
S3.start(0)

# Only start the motors when the inputs go above the following threshold
threshold = 0.60


LeftTrack = 0
RightTrack = 0
x=0
y=0
# Configure the motors to match the current settings.

def setmotors():
        GPIO.output(MotorA0, A0)
        GPIO.output(MotorA1, A1)
        GPIO.output(MotorAE, True)
        GPIO.output(MotorBE, True)
        GPIO.output(MotorB0, B0)
        GPIO.output(MotorB1, B1)

# Try and run the main code, and in case of failure we can stop the motors
try:
    # Turn on the motors
    GPIO.output(MotorAE, True)
    GPIO.output(MotorBE, True)

    # This is the main loop
    while True:

        # Check for any queued events and then process each one
        events = pygame.event.get()
        for event in events:
          UpdateMotors = 0
          print events

          # Check if one of the joysticks has moved
          if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
              LeftTrack = event.value
              UpdateMotors = 1
            elif event.axis == 3:
              RightTrack = event.value
              UpdateMotors = 1
          if event.type == pygame.JOYBUTTONDOWN:
              print 'Etapa 1'
              if event.button == 11:
                  x = 11
                  print x 
                  UpdateMotors = 1
          elif event.type == pygame.JOYBUTTONUP:
              print 'Etapa 1'
              if event.button == 11:
                  x = 0
                  print x 
                  UpdateMotors = 1 
          if event.type == pygame.JOYBUTTONDOWN:
              print 'Etapa 1'
              if event.button == 10:
                  x = 10
                  print x
                  UpdateMotors = 1
          elif event.type == pygame.JOYBUTTONUP:
              print 'Etapa 1'
              if event.button == 10:
                  x = 0
                  print x
                  UpdateMotors = 1

          if event.type == pygame.JOYBUTTONDOWN:
              print 'Etapa 1'
              if event.button == 12:
                  y = 12
                  print y
                  UpdateMotors = 1 
          #elif event.type == pygame.JOYBUTTONDOWN:
          #    print 'Etapa 1'
          #    if event.button == 13:
          #        x = 13
          #        print x
          #        UpdateMotors = 1
          #elif event.type == pygame.JOYBUTTONDOWN:
          #    print 'Etapa 1'
          #    if event.button == 14:
          #        x = 14
          #        print x
          #        UpdateMotors = 1
          #elif event.type == pygame.JOYBUTTONDOWN:
          #    print 'Etapa 1'
          #    if event.button == 15:
          #        x = 15
          #        print x
          #        UpdateMotors = 1


# Check if we need to update what the motors are doing
          if UpdateMotors:
              #if (x==11):
              #    A0 = False
              #    A1 = True
              #    print 'holi'
              if (y==12):
                  if (j.get_button(11) and value < max_val):
                          value = value + 0.5 
                          S1.ChangeDutyCycle(value)
                          print 'To max val:' +  str(value) 
                  elif (j.get_button(10) and value > min_val):
                          value = value - 0.5
                          S1.ChangeDutyCycle(value)
                          print 'To min val' + str(value)
              # Check how to configure the left motor
              # Move forwards
              #if (RightTrack > threshold):
              #    A0 = False
              #    A1 = True 
              # Move backwards
              #elif (RightTrack < -threshold):
              #    A0 = True
              #    A1 = False
              # Stopping
              else:
                  A0 = False
                  A1 = False

              # And do the same for the right motor
              #if (x == 12):
              #    if (j.get_button(11) == 1 and value < max_val):
              #        S1.ChangeDutyCycle(value)
              #        value = value + 1
              #    elif(j.get_button(10) == 1 and value > min_val):
              #        S1.ChangeDutyCycle(value)
              #        value = value - 1
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

              # Now we've worked out what is going on we can tell the
              # motors what they need to do
              setmotors()


except KeyboardInterrupt:
    # Turn off the motors
    GPIO.output(MotorAE, False)
    GPIO.output(MotorBE, False)
    j.quit()#!/usr/bin/env python

GPIO.cleanup()
