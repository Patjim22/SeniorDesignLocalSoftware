#!/usr/bin/python3 -u

# https://stackoverflow.com/questions/19732978/how-can-i-get-a-string-from-hid-device-in-python-with-evdev

import evdev
import RPi.GPIO as GPIO
from evdev import *
import time 
#dev =evdev.InputDevice('/dev/input/by-id/usb-SM_SM-2D_PRODUCT_HID_KBW_APP-000000000-event-kbd')
dev =evdev.InputDevice('/dev/input/by-id/usb-IDTECH_IDTECH_MiniMag_II_USB-HID_Keyboard_Reader-event-kbd')
dev.grab()


# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         print(categorize(event))
# Suppresses warning messages from output.
GPIO.setwarnings(False)
	
	# This tells the library to use the GPIO numbers and not the
	# header pin numbers. If you want to use the pin numbers in
	# the code below, use GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
    
    #add all used gpio pins for configuration
channel_list = (2,3,4,17,22,27,14)
    # Sets up GPIO 2 (Pin 3 as an output) 
GPIO.setup(channel_list, GPIO.OUT)
GPIO.output(channel_list,GPIO.LOW)
    
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

def user_authentication(card):
        
        GPIO.output(2,True)
        global user_1_state
        global user_2_state
        print("Woo a card "+card)
        
        #check user 1
        if ((  user_1_state == 0 ) and (card== str(USER_1) )):
            GPIO.output(4,True)
            user_1_state=1
            print("USER 1")
		#check user 2
        if (( user_2_state == 0 ) and (card== str(USER_2) )):
            GPIO.output(17,True)
            user_2_state=1
            print("USER 2")
            
        if(user_2_state):
            GPIO.output(2,True)
            GPIO.output(3,False)
            print("ACTIVATED")
            GPIO.output(14,True)
            
        
        if((card != str(USER_1)) and (card != str(USER_2))):
            GPIO.output(2,False)
            GPIO.output(3,True)
            GPIO.output(17,False)
            print("DISABLED")
            GPIO.output(14,False)
            user_1_state =0
            user_2_state =0
            
while (True):
    card =input()
    user_authentication(card)


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

#grab provides exclusive access to the device 


#loop 

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

