import sys
from tkinter import *
from tkinter import font
import time
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(40, GPIO.OUT)
#GPIO.output(40, GPIO.LOW)

global start 
global endTime
global countDownText
countDownMinutes=1
endOfWorkingHours=17	#5pm
beginningOfWorkHours=8	#8am
user_1_state = 0
user_2_state = 0

countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is

#GPIO.setwarnings(False)                         # Suppresses warning messages from output.
#GPIO.setmode(GPIO.BCM)                          # Use GPIO Pin numbers instead on Board pin numbers
    
    # Add all used gpio pins for configuration
    #22 is green LED device On
    #27 user 1 #17 user 2 yellow LEDs
    #4 and 3  RED LEDS
    #2 control opto
    #14 usb sel
DEVICEON =22
USER1LED =27
USER2LED=17
REDLED1 =4
REDLED2 =3
CONTROLOPTO =2
USBSEL =14
RESETBUTTON = 18


channel_list = (2,3,4,17,22,27,14)              # Pin 2 needs changed
    # Sets all GPIO pins in the chanel list as an output
#GPIO.setup(channel_list, GPIO.OUT, initial =GPIO.LOW)

#GPIO.setup(RESETBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)#sets the reset to a input with a pull up resistor
   
#GPIO.output(DEVICEON,FALSE)                            # Set power pin to on
    # Set switch pin to defaults
#GPIO.output(USBSEL,False)                            # USB
#GPIO.output(CONTROLOPTO,False)                            # Opto-Isolator

    # Give scanner time to get online
print("INITIALIZED")



def ledON():
	print("LED button pressed")
	start = time.ctime(time.time())
	print(start)
	#if GPIO.input(40) :
	#	GPIO.output(40,GPIO.LOW)
	ledButton["text"] = "LED ON"
	#else:
	#	GPIO.output(40,GPIO.HIGH)
	#ledButton["text"] = "LED OFF"

def exitProgram():
	print("Exit Button pressed")
	#GPIO.cleanup()
	win.quit()	
 
def countdown():
	currentTime =endTime-time.time()
	#print(int(currentTime/60),":", int(currentTime%60))
	countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)))
	#countDown.config(text=str(int(currentTime))+":")
	#print(str(time.localtime().tm_hour) +":"+str(time.localtime().tm_min))
	
	
	#time.sleep(1)
	win.update()
	
def configurePi():
    #pull config data from SQL database
    return

def enableDevice():
	#GPIO.output(CONTROLOPTO,True)              # Opto
	#GPIO.output(USBSEL,True)                 	# USB
	print("ACTIVATED")
	#GPIO.output(DEVICEON,True)                	# Device enable light
	endTime = time.time()+countDownIncrementer

def disableDevice():
    #GPIO.output(CONTROLOPTO,False)             # Opto
    #GPIO.output(USBSEL,False)                	# USB
    #GPIO.output(USER2LED,False)               	# User 2 led
    #GPIO.output(USER1LED,False)                # User1 led
    print("DISABLED")
    print("Invalid user")
    #GPIO.output(DEVICEON,False)               	# Device enable light
    user_1_state =0
    user_2_state =0

    

win = Tk()

myFont = font.Font(family = 'Helvetica', size = 84, weight = 'bold')
#config column rows and col
Grid.rowconfigure(win,0, weight=1)
Grid.rowconfigure(win,1, weight=1)
Grid.columnconfigure(win,0,weight=1)
 
win.title("Access Control")#window name
win.geometry('800x480')#size of window
countDownText = "count"
countDown = Label(win,text= countDownText ,anchor=CENTER,font= myFont) #create label for countdown
#countDown.pack()
countDown.grid(row=0,column=0, sticky="nsew")#puts the countdown to the center of the screen
exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =2 , width = 6) 
#exitButton.pack(side = BOTTOM)

ledButton = Button(win, text = "LED ON", font = myFont, command = ledON, height = 2, width =8 )
ledButton.grid(row=1)
#ledButton.pack()
#if( (int(time.ctime(time.time()))>=17 )and (int(time.ctime(time.time()))<=8) ):
	#print(time.ctime(time.time()))
endTime = time.time()+countDownIncrementer


 
while True:
	if time.time() <= endTime:
		countdown()
	card = sys.stdin
	if(time.localtime().tm_hour<endOfWorkingHours and time.localtime().tm_hour >=beginningOfWorkHours):#between 8am and 5pm only 1 user is needed
		if(user_1_state or user_2_state):
			enableDevice()
			print("use time: " + str((endTime-time.time())/60) +"minutes")
           
		else:#outside of normal hours a buddy is required
			print("A buddy is required")
			if(user_1_state and user_2_state):
				enableDevice()
			else:
				print("another user is required")


