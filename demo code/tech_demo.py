#tech_demo.py
import sys
import RPi.GPIO as GPIO
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
        
        print("INITIALIZED")
        #print(get_scanner.x)
        card= 0
        GPIO.output(2,True)
        #check user 1
        if (( user_1_state == 0 ) and (card== USER_1 )):
            GPIO.output(4,True)
            user_1_state=1
            print("USER 1")
		#check user 2
        if (( user_2_state == 0 ) and (card== USER_2 )):
            GPIO.output(17,True)
            user_2_state=1
            print("USER 2")
            
        if(user_1_state):
            GPIO.output(2,True)
            GPIO.output(3,False)
            print("ACTIVATED")
            GPIO.output(14,True)
        if((card != USER_1) and (card != USER_2)):
            GPIO.output(2,False)
            GPIO.output(3,True)
            print("DISABLED")
            GPIO.output(14,False)
            user_1_state =0
            user_2_state =0
            
        
    