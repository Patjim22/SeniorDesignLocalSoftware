import RPi.GPIO as GPIO

BUTTON1 = 29
BUTTON2 = 31

GPIO.setmode(GPIO.BOARD)                                   #Use Board pin numbers
GPIO.setwarnings(False)
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while(True):
    if(GPIO.input(BUTTON1)==GPIO.LOW):
        print("Button 1")
        
    if(GPIO.input(BUTTON2)==GPIO.LOW):
        print("Button 2")
        
