import RPi.GPIO as GPIO
import time
import datetime
import math
from ISStreamer.Streamer import Streamer
streamer = Streamer("Hamster Fitness Tracker", client_key="PUT YOUR CLIENT KEY HERE")
streamer.log("ZooZoo Says","")

# Setup Pins
pinNumLaserBreak = 18
pinNumLED = 4
GPIO.setmode(GPIO.BCM) # numbering scheme that corresponds to breakout board and pin layout
GPIO.setup(pinNumLaserBreak,GPIO.IN)
GPIO.setup(pinNumLED,GPIO.OUT)

# Setup Constants
diameter = 13 # inches
circumference = diameter * math.pi * 0.0000157828283 # miles
distanceTotal = 0
timeNoActivity = 5 # seconds

speed = 0
lastTime = datetime.datetime.now()
while True:
  input = GPIO.input(pinNumLaserBreak)
  if not input:
    if speed == 0:
      streamer.log("ZooZoo Says", "It's time to get pumped")

    # Calculate stuff
    thisTime = datetime.datetime.now()
    timeDiff = (thisTime-lastTime).total_seconds()
    speed = circumference/(timeDiff/3600) # miles per hour

    # Log stuff
    streamer.log("Full Rotation", "1")
    if speed < 5: # Filter out glitches (rocking on the sensor)
      distanceTotal += circumference
      streamer.log("Speed(mph)", speed)
      streamer.log("Total Distance(miles)", distanceTotal)

    GPIO.output(pinNumLED,GPIO.HIGH) # Turn LED on for visual cue that everthing is working
    lastTime = thisTime

    # Wait for sensor break to clear
    input = GPIO.input(pinNumLaserBreak)
    while not input:
      input = GPIO.input(pinNumLaserBreak)
      time.sleep(.05)
  else:
    if speed > 0:
      thisTime = datetime.datetime.now()
      timeDiff = (thisTime-lastTime).total_seconds()

      # Reset the speed to 0 if no activity (for log visualization)
      if timeDiff > timeNoActivity:
        speed = 0
        # Log stuff
        streamer.log("ZooZoo Says", "I need a rest")
        streamer.log("Speed(mph)", speed)
        streamer.flush()

    GPIO.output(pinNumLED,GPIO.LOW) # Turn LED off for visual cue that everthing is working

