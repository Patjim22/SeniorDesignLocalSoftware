#tech_demo.py
import sys
import RPI.GPIO as GPIO
import get_scanner

def main(argv):
    # Suppresses warning messages from output.
    GPIO.setwarnings(False)
	
	# This tells the library to use the GPIO numbers and not the
	# header pin numbers. If you want to use the pin numbers in
	# the code below, use GPIO.setmode(GPIO.BOARD)
    GPIO.setmode(GPIO.BCM)
    
    #add all used gpio pins for configuration
    channel_list = [2,3,4,17,27,14]
    # Sets up GPIO 2 (Pin 3 as an output) 
    GPIO.setup(channel_list, GPIO.OUT)
    
    # Define constants and variables

    USER_1=200338060
    USER_2=200248706
    
    user_1_state=0
    user_2_state=0
    
    # Set power pin to on
    GPIO.output(27,True)
    # Set switch pin to default
    GPIO.output(3,True)

    # Give scanner time to get online
    print("INITIALIZED")

    # Pipe scanner input to subshell
    while True:
        print(get_scanner.x)
        GPIO.output(2,True)
    