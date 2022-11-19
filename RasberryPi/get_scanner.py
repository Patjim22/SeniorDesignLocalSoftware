#!/usr/bin/python3 -u
                                                # this tells the Pi to use Python3 instead of Python 2

# https://stackoverflow.com/questions/19732978/how-can-i-get-a-string-from-hid-device-in-python-with-evdev
                                                # location at which teh keycard reader code was found
import evdev
import RPi.GPIO as GPIO
from evdev import *
import time 

#dev =evdev.InputDevice('/dev/input/by-id/usb-SM_SM-2D_PRODUCT_HID_KBW_APP-000000000-event-kbd')
dev =evdev.InputDevice('/dev/input/by-id/usb-IDTECH_IDTECH_MiniMag_II_USB-HID_Keyboard_Reader-event-kbd')
dev.grab()                                      # Grab provides exclusive access to the device 

GPIO.setwarnings(False)                         # Suppresses warning messages from output.
GPIO.setmode(GPIO.BCM)                          # Use GPIO Pin numbers instead on Board pin numbers
#GPIO.setmode(GPIO.Board)
    
    # Add all used gpio pins for configuration
channel_list = (2,3,4,17,22,27,14)              # Pin 2 needs changed
    # Sets all GPIO pins in the chanel list as an output
GPIO.setup(channel_list, GPIO.OUT)
GPIO.output(channel_list,GPIO.LOW)

    # Define constants and variables
USER_1=200338060
USER_2=200248706
   
user_1_state = 0
user_2_state = 0
    
GPIO.output(27,True)                            # Set power pin to on
    # Set switch pin to defaults
GPIO.output(3,False)                            # USB
GPIO.output(2,False)                            # Opto-Isolator

    # Give scanner time to get online
print("INITIALIZED")

    # Main section of code used for authentication:
def user_authentication(card):
        
        global user_1_state
        global user_2_state
        # why are the globals defined inside the function?
        # when we test this, we should move around the functions and definitions 

        print("Woo a card "+card)
        
        if((card != str(USER_1)) and (card != str(USER_2))):
            GPIO.output(2,False)                # Opto
            GPIO.output(3,False)                # USB
            GPIO.output(17,False)               # User 2 led
            GPIO.output(4,False)                # User1 led
            print("DISABLED")
            GPIO.output(14,False)               # Device enable light
            user_1_state =0
            user_2_state =0
            
        #check user 1
        if ((  user_1_state == 0 ) and (card== str(USER_1) )):
            GPIO.output(4,True)                 # User 1 led
            user_1_state=1
            print("USER 1")
		#check user 2
        if (( user_2_state == 0 ) and (card== str(USER_2) )):
            GPIO.output(17,True)                # User 2 led
            user_2_state=1
            print("USER 2")
            
        if(user_2_state):
            GPIO.output(2,True)                 # Opto
            GPIO.output(3,True)                 # USB
            print("ACTIVATED")
            GPIO.output(14,True)                # Device enable light
            
        

    # Test code for keyboard input instead of the keycard reader
while (True):
    card =input()
    print(card)
    user_authentication(card)



    # ASCII Definitions for the Keycard Reader interpretation:
scancodes = { 
    # Scancode: ASCIICode 
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r', 
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL', 
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';', 
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n', 
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
} 

capscodes = { 
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*', 
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R', 
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL', 
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':', 
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N', 
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
} 
#setup vars 
x = '' 
caps = False 


    # Loop for the Keycard Reader:
# for event in dev.read_loop(): 
#     if event.type == ecodes.EV_KEY: 
#      data = categorize(event) # Save the event temporarily to introspect it 
#      if data.scancode == 42: 
#       if data.keystate == 1: 
#        caps = True 
#       if data.keystate == 0: 
#        caps = False 
#      if data.keystate == 1: # Down events only 
#       if caps: 
#        key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
#       else: 
#        key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
#       if (data.scancode != 42) and (data.scancode != 28): 
#        x += key_lookup 
#       if(data.scancode == 28): 
#        print (x)   # Print it all out! 
#        user_authentication(x)
#        x = ''

