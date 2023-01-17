
import RPi.GPIO as GPIO

DEVICEON =22
USER1LED =27
USER2LED=17
REDLED1 =4
REDLED2 =3
CONTROLOPTO =2
USBSEL =14
RESETBUTTON = 18


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