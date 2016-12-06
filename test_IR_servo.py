import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import time

ADC.setup()

GPIO.setup("P8_7", GPIO.OUT)
GPIO.output("P8_7", GPIO.HIGH)

servo_pin = "P8_13"
duty_min = 3.5#3
duty_max = 14.5#14.5
duty_span = duty_max - duty_min

angle = 0 
direction = "left"

PWM.start(servo_pin, (100-duty_min), 60.0,1)
angle_f = float(angle)
duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
 
PWM.set_duty_cycle(servo_pin, duty)

while 1:
    voltage0 = ADC.read_raw("AIN0")

    angle_f = float(angle)
    duty = 100 - ((angle_f / 180) * duty_span + duty_min) 
    PWM.set_duty_cycle(servo_pin, duty)

    print("IR_Voltage" , voltage0)
    print("Angle" , angle)
    time.sleep(0.1)

    if angle < 180:
        if direction == "left":
            angle = angle + 1
        if direction == "right":
            if angle < 1:
                direction = "left"
                angle = angle +1
            else:
                angle = angle -1
    else:
        direction = "right"
        angle = angle -1
