import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)                                   #Use Board pin numbers
GPIO.setwarnings(False)
GPIO.setup(37, GPIO.OUT, initial =GPIO.LOW)
GPIO.output(37,True) 