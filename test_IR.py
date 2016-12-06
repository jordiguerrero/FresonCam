import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

import time

ADC.setup()

GPIO.setup("P8_7", GPIO.OUT)
GPIO.output("P8_7", GPIO.HIGH)
while 1:
    voltage0 = ADC.read_raw("AIN0")
#    voltage1 = ADC.read_raw("AIN1")
#    voltage2 = ADC.read_raw("AIN2")
#    voltage3 = ADC.read_raw("AIN3")
#    voltage4 = ADC.read_raw("AIN4")
#    print("0-1-2-3-4" , voltage0, voltage1, voltage2, voltage3, voltage4)
    print("0-1-2-3-4" , voltage0)
    time.sleep(0.1)
