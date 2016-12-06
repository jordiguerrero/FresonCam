from Fresonbot import Fresonbot
import time

t = 1
R1 = Fresonbot()

print ("Drive forward for 1 seconds")
R1.motion(50,50)
time.sleep(t)

print ("Drive backward for 1 seconds")
R1.motion(-50,-50)
time.sleep(t)

print ("Turn left for 1 seconds")
R1.motion(-50,50)
time.sleep(t)

print ("Turn right for 1 seconds")
R1.motion(50,-50)
time.sleep(t)


R1.stop()
