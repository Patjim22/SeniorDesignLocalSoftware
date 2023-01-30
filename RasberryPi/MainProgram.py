import threading
import time
import sys
import re
from tkinter import *
from tkinter import font
#import RPi.GPIO as GPIO

card = "0"
global start 
global endTime 
endTime=0
global countDownText
global user_1_state, user_2_state
userName =""
countDownMinutes=1
endOfWorkingHours=17	#5pm
beginningOfWorkHours=8	#8am
user_1_state =0
user_2_state = 0
user_1_ID = 0
user_2_ID = 0




    
# Add all used gpio pins for configuration
DEVICEON =9                                     #22 is green LED device On
USER1LED =11                                    #27 user 1 #17 user 2 yellow LEDs
USER2LED=13
REDLED1 =19                                     #4 and 3  RED LEDS
REDLED2 =26
CONTROLOPTO =17                                 #2 control opto
USBSEL =14                                      #14 usb sel
USBENABLE = 15
RESETBUTTON = 18
BUTTON1 = 5
BUTTON2 = 6

BackUp_USER= {"200248706", "200289830"}
channel_list = (5,6,9,11,13,14,15,17,18,19,26)              # Pin 2 needs changed

class ID_Check_Thread (threading.Thread):
    
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
    # helper function to execute the threads
    def run(self):
        global card
        while True:
            if(card!='0'):
                print("Reading user card")
                assignUserToMachine(card)
                card ="0"
                
                
            time.sleep(2)

class ReadCardTread (threading.Thread): #reads the card
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    # helper function to execute the threads
    def run(self):
        global card
        for line in sys.stdin:
            if  'q' == line.rstrip():
                break
            regSearch =re.compile('\+.*')
            cardNumber = regSearch.match(line)
            #print(cardNumber)
            if(cardNumber!=None):
                card = cardNumber.string[1:10].rstrip()
                print(cardNumber.group()[1:10].rstrip())
                print()
            else:
                print(len(line))
                if(len(line)==10):
                    card = line[0:9]
                    print(line[0:9])
            sys.stdin.flush
            time.sleep(4)
            
def setupGPIO():
    #GPIO.setmode(GPIO.BOARD)                                   #Use Board pin numbers
    #GPIO.setwarnings(False)                                    # Suppresses warning messages from output.
    # Sets all GPIO pins in the chanel list as an output
    #GPIO.setup(channel_list, GPIO.OUT, initial =GPIO.LOW)
    #GPIO.setup(RESETBUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets the reset to a input with a pull up resistor
    #GPIO.output(DEVICEON,FALSE)                                # Set power pin to on
    # Set switch pin to defaults
    #GPIO.output(USBSEL,False)                                  # USB
    #GPIO.output(CONTROLOPTO,False)                             # Opto-Isolator
    print("GPIO SETUP")

def countdown(): #does the countdown when it is required
    global endTime
    currentTime =endTime-time.time()                            #measures the endtime vs current time
    #currentTime = time.time()
    if(currentTime >0):
        countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)))
    else:
        endTime =0
	
def configurePi():#pull config data from SQL database
    countDownMinutes # should be editable to change the length of the countdown
    endOfWorkingHours # changes the end time of the makerspace working hours
    beginningOfWorkHours # changes the start time of the makerspace working hours
    return

def enableDevice(): #enables the usb and Control OPTO issolators and starts the countdown
	global endTime
    #GPIO.output(CONTROLOPTO,True)              # Opto
	#GPIO.output(USBSEL,True)                 	# USB
	print("ACTIVATED")
	#GPIO.output(DEVICEON,True)                	# Device enable light
	endTime = time.time()+countDownIncrementer

def disableDevice():
    global user_1_state , user_2_state,user_2_ID, user_1_ID, endTime
    #GPIO.output(CONTROLOPTO,False)             # Opto
    #GPIO.output(USBSEL,False)                	# USB
    #GPIO.output(USER2LED,False)               	# User 2 led
    #GPIO.output(USER1LED,False)                # User1 led
    print("DISABLED")
    #GPIO.output(DEVICEON,False)               	# Device enable light
    user_1_state =0
    user_2_state =0
    user_1_ID =0
    user_2_ID =0
    
    endTime=0

def pauseDevice():#disables optoControl
    #GPIO.output(CONTROLOPTO,False)             # Opto
    print("Paused device")

def check_if_authorized(card):
    USERS ={"100019744","100019747"} #visitor 1 id #visitor 4 id
    #write user compatison code for sql in this
    userName
    if card in BackUp_USER:
        enableDevice()
        return True
    if card in USERS:
        return True
    return False	# function returns true if authorized user otherwise false

def assignUserToMachine(card):
    global user_1_state , user_2_state, user_1_ID, user_2_ID
    authorized = check_if_authorized(card)
    if(authorized):
        if(user_1_state==0):
            user_1_state=1
            user_1_ID= card
        if(user_1_state==1):
            if(card != user_1_ID):
                user_2_state=1
                user_2_ID = card
        if(time.localtime().tm_hour<endOfWorkingHours and time.localtime().tm_hour >=beginningOfWorkHours):#during working houres only 1 user is needed
            if(user_1_state or user_2_state):
                enableDevice()     
        else:#outside of normal hours a buddy is required
            if(user_1_state and user_2_state):
                enableDevice()
            else:
                print("A buddy is required")        #needs to write to a label on the gui     
    else:
        print("non-authorized user")

T1 = True
T2 = True
configurePi()
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
countDown.grid(row=0,column=0, sticky="nsew")#puts the countdown to the center of the screen

ledButton = Button(win, text = "LED ON", font = myFont, height = 2, width =8 )
ledButton.grid(row=1)
#endTime = time.time()+countDownIncrementer

disableDevice()

countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is
th1=  ID_Check_Thread("T1",1000)
th2 = ReadCardTread("T2",2000)
th1.start()
th2.start()

while T1:
    if(endTime!=0):
        countdown()
    else:
        #countDown.config(text=str(time.localtime().tm_hour%12) +":"+str(time.localtime().tm_min))
        countDown.config(text= time.strftime("%I:%M:%S")) 
    win.update()
    #if(input().rstrip()=="q"):
    #    T1 = False
    #   T2 = False
    #    break
    #print("Hello " +str(T1))
    time.sleep(.5)   

win.destroy()
print("Exit")