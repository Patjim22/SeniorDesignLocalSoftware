
import RPi.GPIO as GPIO

def disableDevice():
    GPIO.output(CONTROLOPTO,False)             # Opto
    GPIO.output(USBSEL,False)                	# USB
    GPIO.output(USER2LED,False)               	# User 2 led
    GPIO.output(USER1LED,False)                # User1 led
    print("DISABLED")
    print("Invalid user")
    GPIO.output(DEVICEON,False)               	# Device enable light
    user_1_state =0
    user_2_state =0
    
    
disableDevice()