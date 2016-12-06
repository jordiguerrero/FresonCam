import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO

import time
import math
import subprocess

import pinout # pinout.py is where I defined all used pins in BBB
from Fresonbot import Fresonbot

robot1 = Fresonbot() # Using Fresonbot class

# Use it variable to describe your trajectory ([x1,y2,x2,y2,....,xn,yn])
#it = iter([400,0,400,400,0,400,200,200,0,0,400,0,400,400,0,400,200,200,0,0])
#it = iter([400,0,400,400,0,400,200,200,0,0])
#it = iter([200,0,200,200,0,200,0,0])
it = iter([100,0,100,100,0,100,0,0])
#it = iter([200,100])

# PID constants
#Kp = 150
#Ki = 0.1
#Kd = 0.001
Kp = 200
Ki = 0.0
Kd = 0.0

#Change velocityTranslational to increase or decrease velocity
velocityTranslational = 70 

def changeHeading():
    global u
    global headingError
    global headingErrorDerivative
    global headingErrorIntegral
    global lastHeadingError
    global VelLeft
    global VelRight

    deltax = xTarget - robot1.x
    deltay = yTarget - robot1.y

    referenceHeading =  math.atan2(deltay, deltax)
#    headingError = referenceHeading - robot1.heading
    headingError = (referenceHeading - robot1.heading+ math.pi)%(2*math.pi) - math.pi

    headingErrorDerivative = (headingError - lastHeadingError) / dt
    headingErrorIntegral += (headingError * dt)
    lastHeadingError = headingError

    u = (Kp * headingError) + (Ki * headingErrorIntegral) + (Kd * headingErrorDerivative)

    VelLeft = (velocityTranslational + u)
    VelRight = (velocityTranslational - u)

    return

def goTarget():
    global start_dt
    global dt
    global xTarget
    global yTarget

    while ((robot1.x > xTarget + sensitivityLimit) or (robot1.x < xTarget - sensitivityLimit)) or ((robot1.y > yTarget + sensitivityLimit) or (robot1.y < yTarget - sensitivityLimit)):

        end_dt = time.time() * 1000
        dt = end_dt - start_dt
        start_dt = end_dt

        robot1.getPosition();

        changeHeading();

        robot1.motion(VelLeft, VelRight)

        time.sleep(0.02)
    return

#Initializing variables
IncTicksLeft = 0
IncTicksRight = 0
distanceLeft = 0
distanceRight = 0
lastHeadingError = 0
headingErrorIntegral = 0
sensitivityLimit = 5
u = 0
VelLeft = velocityTranslational
VelRight = velocityTranslational

#Main program
robot1.getTicks();

start_dt = time.time() * 1000

robot1.motion(velocityTranslational,velocityTranslational)

time.sleep(0.02)

robot1.getPosition();

for xT, yT in zip(it, it):
    xTarget = xT
    yTarget = yT

    goTarget();

robot1.stop();

time.sleep(0.5)

robot1.getTicks();

robot1.getPosition();
