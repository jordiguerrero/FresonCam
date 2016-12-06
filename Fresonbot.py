import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
#import Adafruit_BBIO.ADC as ADC #IR
import subprocess
import math

import pinout 


class Fresonbot(object):

    ticksPerTurn = 12 *100 # 12 counts per revolution * 100:1 reduction gearbox
## you have to take this measures accurately
#    WheelRadius = 31.8/2 # I took the diameter and divided by 2
#    WheelDistance = 88.9 # between centers
    WheelRadius = 16 # In mm
    WheelDistance = 89 # In mm

    duty_min = 3
    duty_max = 14
    duty_span = duty_max - duty_min


    def __init__(self):

        subprocess.call("bashScripts/enable_encoder_slots.sh")

        GPIO.setup(pinout.PinMotorLeftPhase, GPIO.OUT)
        GPIO.setup(pinout.PinMotorRightPhase, GPIO.OUT)
        GPIO.output(pinout.PinMotorLeftPhase, 0)
        GPIO.output(pinout.PinMotorRightPhase, 0)
        PWM.start(pinout.PinMotorLeftPwm,0)
        PWM.start(pinout.PinMotorRightPwm,0)

        self.x = 0.0
        self.y = 0.0
        self.distance = 0.0
        self.heading = 0.0
        (TicksLeft, TicksRight) = self.getTicks();
        self.StartTicksLeft = TicksLeft 
        self.StartTicksRight = TicksRight 
#        ADC.setup() # IR

    def motion(self,VelLeft,VelRight):
        AbsVelLeft = abs(VelLeft)
        AbsVelRight = abs(VelRight)
        if (VelLeft < 0):
            PhaseLeft = 1
        else:
            PhaseLeft = 0
        if (VelRight < 0):
            PhaseRight = 1
        else:
            PhaseRight = 0
        if (AbsVelLeft > 100):
            AbsVelLeft = 100
        if (AbsVelRight > 100):
            AbsVelRight = 100

        GPIO.output(pinout.PinMotorLeftPhase, PhaseLeft)
        GPIO.output(pinout.PinMotorRightPhase, PhaseRight)
        PWM.set_duty_cycle(pinout.PinMotorLeftPwm,AbsVelLeft)
        PWM.set_duty_cycle(pinout.PinMotorRightPwm,AbsVelRight)
        return 


    def getTicks(self):
        global TicksLeft
        global TicksRight

        fTicksLeft = "/sys/devices/ocp.3/48302000.epwmss/48302180.eqep/position"
        fTicksRight = "/sys/devices/ocp.3/48304000.epwmss/48304180.eqep/position"
        foTicksLeft = open(fTicksLeft, "r")
        foTicksRight = open(fTicksRight, "r")

        TicksLeft = foTicksLeft.read()
        TicksLeft = int(TicksLeft.split('\n', 1)[0])
        TicksRight = foTicksRight.read()
        TicksRight = int(TicksRight.split('\n', 1)[0])

        foTicksLeft.close()
        foTicksRight.close()

        return TicksLeft, TicksRight

    def getPosition(self):

        (TicksLeft, TicksRight) = self.getTicks()
        EndTicksLeft = TicksLeft
        EndTicksRight = TicksRight

        IncTicksLeft = EndTicksLeft - self.StartTicksLeft
        IncTicksRight = EndTicksRight - self.StartTicksRight

        distanceLeft = 2 * math.pi * self.WheelRadius * (float(IncTicksLeft) / self.ticksPerTurn)
        distanceRight = 2 * math.pi * self.WheelRadius * (float(IncTicksRight) / self.ticksPerTurn)

        newdistance = (distanceLeft + distanceRight) / 2
        self.distance += newdistance

        self.heading += (distanceLeft - distanceRight) / self.WheelDistance
        self.x += newdistance * math.cos(self.heading)
        self.y += newdistance * math.sin(self.heading)
        self.headingDec = math.degrees(self.heading)

        self.StartTicksLeft = EndTicksLeft
        self.StartTicksRight = EndTicksRight

        return (self.x, self.y, self.heading,self.distance)


    def stop(self):
        self.motion(0,0);

        return

#    def readIR(self):
#        voltage = ADC.read(pinout.PinIRFront)
##        return value1 * 1.8
#        return 3.07427335017539*voltage**-1.18207892010248


