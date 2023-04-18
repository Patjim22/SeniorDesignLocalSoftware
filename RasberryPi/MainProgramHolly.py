#!/bin/python3
import threading
import time
import sys
import re
from tkinter import *
from tkinter import font
# import requests
# import json
# import os
# from getmac import get_mac_address
# import RPi.GPIO as GPIO
# import evdev
# from evdev import *
#from sql_connection import *

#API_HEADERS = { "MAC" : get_mac_address() }

card = "0"
global start 
global endTime 
endTime=0
global countDownText
global user_1_state, user_2_state
twoSwipeTime = 20        #used to hold how long to wait for a buddy to swipe
buddySwipeReuiredBy=0   #holds the time to cancel out and say you were rejected because no buddy
userName =""
countDownMinutes=2.1
countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is
endOfWorkingHours=17	#5pm
beginningOfWorkHours=8	#8am
TIMETOTURNBUZZERON =10 #in seconds
TIMESTOBUZ = {5,2,1,.33}    #this is the times for the buzzer to buzz at this is in minutes
user_1_state =0
user_2_state = 0
user_1_ID = 0
user_2_ID = 0
global gui_state
gui_state=0
global gui_flag
gui_flag=0




    
# Add all used gpio pins for configuration
DEVICEON =21                                     #22 is green LED device On
USER1LED =23                                    #27 user 1 #17 user 2 yellow LEDs
USER2LED=33
DEVICEENABLED =35                                     #4 and 3  RED LEDS
EXTERNALRELAY =37
CONTROLOPTO =11                                 #2 control opto
USBSEL =8                                      #14 usb sel changes which usb port on pcb is being used 1 is port 2 which is the port the device is plugged in to and 0 is the other port that is not in use
USBENABLE = 10                                  #when high disables usb ports on pcb
BUZZER = 12
BUTTON1 = 29                                    #reset device 
BUTTON2 = 31                                    #top panel button

BackUp_USER= {"200248706", "200289830"}
channel_list = (21,23,33,35,37,11,8,10,12,29,31)              



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
                print("checking ID")
                assignUserToMachine(card)
                card ="0"
            time.sleep(2)   #sleep 2 seconds

class Read_Card_Tread (threading.Thread): #reads the card
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
#     # ASCII Definitions for the Keycard Reader interpretation:
#     scancodes = { 
#     # Scancode: ASCIICode 
#     0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8', 
#     10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r', 
#     20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL', 
#     30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';', 
#     40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n', 
#     50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
# } 

#     capscodes = { 
#     0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*', 
#     10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R', 
#     20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL', 
#     30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':', 
#     40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N', 
#     50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT' 
# } 
#         #setup vars 
#         line = '' 
#         caps = False 

#         dev =evdev.InputDevice('/dev/input/event0')
#         dev.grab()

#         for event in dev.read_loop():
#             if event.type == ecodes.EV_KEY: 
#                 data = categorize(event) # Save the event temporarily to introspect it 
#                 if data.scancode == 42: 
#                  if data.keystate == 1: 
#                   caps = True 
#                  if data.keystate == 0: 
#                   caps = False 
#                 if data.keystate == 1: # Down events only 
#                     if caps: 
#                      key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
#                     else: 
#                      key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode) # Lookup or return UNKNOWN:XX 
#                     if (data.scancode != 42) and (data.scancode != 28): 
#                      line += key_lookup 
#                     if(data.scancode == 28): 
#                      print (line)   # Print it all out!
#                      rshiftCheck=False 
#                      regSearch =re.compile('\+.*')
#                      cardNumber = regSearch.match(line)
#                      if(cardNumber==None):
#                         rshiftCheck =True
#                         regSearch =re.compile('RSHFT=.*')
#                         cardNumber = regSearch.match(line)
#                      print(cardNumber)
#                      if(cardNumber!=None):
#                         card = cardNumber.string[1:10].rstrip()
#                         #print(cardNumber.group()[1:10].rstrip())
#                         if(rshiftCheck):
#                             card = cardNumber.string[6:15].rstrip()
#                             print(card)
#                         print()
#                      else:
#                         #print(len(line))
#                         if(len(line)==9):
#                             card = line[0:9]
#                             print(line[0:9])
#                      line = ''
#             
            
def setupGPIO():
    # GPIO.setmode(GPIO.BOARD)                                   #Use Board pin numbers
    # GPIO.setwarnings(False)                                    # Suppresses warning messages from output.
    # # Sets all GPIO pins in the chanel list as an output
    # GPIO.setup(channel_list, GPIO.OUT, initial =GPIO.LOW)
    # GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets the reset to a input with a pull up resistor
    # GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets the reset to a input with a pull up resistor
    # GPIO.output(DEVICEON,True)                                # Set power pin to on
    # # Set switch pin to defaults
    # GPIO.output(USBSEL,False)                                  # USB
    # GPIO.output(USBENABLE,False)
    # GPIO.output(CONTROLOPTO,False)                             # Opto-Isolator
    print("GPIO SETUP")

def countdown(): #does the countdown when it is required
    global endTime
    currentTime =endTime-time.time()                            #measures the endtime vs current time
    #currentTime = time.time()
    if(currentTime >0):
        buzzEnable = False
        for value in TIMESTOBUZ:
            if(currentTime <= value*60 and currentTime >= value*60 - TIMETOTURNBUZZERON):
                #GPIO.output(BUZZER,True)
                print("Buzz"+str(value))
        if buzzEnable == False :
            #GPIO.output(BUZZER,True)
            pass
        countDown.config(text=str(int(currentTime/60)) +":" +str("{:02d}".format(int(currentTime%60))))
    else:
        endTime =0
        #GPIO.output(BUZZER, False)
        disableDevice()
	
def enableDevice(): #enables the usb and Control OPTO issolators and starts the countdown
    global endTime
    # GPIO.output(CONTROLOPTO,True)              # Opto
    # GPIO.output(USBSEL,True)                 	# USB
    # GPIO.output(USBENABLE, False)
    # GPIO.output(EXTERNALRELAY, True)
    print("ACTIVATED")
    # GPIO.output(DEVICEENABLED,True)                	# Device enable light
    endTime = time.time()+countDownIncrementer
    #SessionStarted()                            

def disableDevice():
    global user_1_state , user_2_state,user_2_ID, user_1_ID, endTime, userName
    # GPIO.output(CONTROLOPTO,False)             # Opto
    # GPIO.output(USBSEL,False)                	# USB
    # GPIO.output(USBENABLE, True)
    # GPIO.output(EXTERNALRELAY, False)
    # GPIO.output(USER2LED,False)               	# User 2 led
    # GPIO.output(USER1LED,False)                # User1 led
    print("DISABLED")
    #GPIO.output(DEVICEENABLED,False)               	# Device enable light
    #GPIO.output(BUZZER, False)
    user_1_state =0
    user_2_state =0
    user_1_ID =0
    user_2_ID =0
    userName =""
    endTime=0
    SessionEnded()

def pauseDevice():#disables optoControl
    #GPIO.output(CONTROLOPTO,False)             # Opto
    print("Paused device")

def check_if_authorized(card):
    global userName, user_1_state, user_2_state
    USERS ={"100019744","100019747"} #visitor 1 id #visitor 4 id
    #write user compatison code for sql in this
    userName
    if card in BackUp_USER:
        userName = "Admin"
        user_1_state=1
        user_2_state=1
        return True
    if card in USERS:
        return True
    return False	# function returns true if authorized user otherwise false

def check_if_admin(card):
    pass

def assignUserToMachine(card):
    global user_1_state , user_2_state, user_1_ID, user_2_ID, buddySwipeReuiredBy, gui_state
    authorized = check_if_authorized(card)
    if(card in BackUp_USER):    #checks if card is a backup user in the system and then activates machine
        user_1_state =1
        user_2_state=1
        user_1_ID = card
        # GPIO.output(USER1LED,True)
        # GPIO.output(USER2LED,True)
        authorized = True
        enableDevice()
        gui_state=1
        return
    if(endTime != 0):           #if machine is running check to see if it is the user currently swiped in
            if(user_1_ID ==card or user_2_ID == card):  #if the card is user1 or user 2's replace user 1 with that card
                user_1_state =1
                user_1_ID =card     #sets user1 ID to be card number
                user_2_state=0
                user_2_ID =""
            elif(check_if_admin(card)):             #admin user state
                user_1_ID = card    #admin card number replaces user1
                user_1_state =1     
                user_2_ID =card     #admin card number replaces user2
                user_2_state =1
            else:
                authorized = False
                print("Another user is currently using the machine")
    if(authorized):
        if(user_1_state==0):
            user_1_state=1
            user_1_ID= card
            #GPIO.output(USER1LED,True)
        if(user_1_state==1):
            if(card != user_1_ID):
                user_2_state=1
                user_2_ID = card
                buddySwipeReuiredBy=0
                #GPIO.output(USER2LED,True)
        if(time.localtime().tm_hour<endOfWorkingHours and time.localtime().tm_hour >=beginningOfWorkHours):#during working houres only 1 user is needed
            if(user_1_state or user_2_state):
                gui_state=1
                enableDevice()     
        else:#outside of normal hours a buddy is required
            if(user_1_state and user_2_state):
                enableDevice()
                gui_state=1
            else:
                print("A buddy is required")        #needs to write to a label on the gui
                gui_state=1
                buddySwipeReuiredBy=time.time()+twoSwipeTime     
    else:
        print("non-authorized user")
        gui_state=2
        
        

def noBuddySwipe():#send to database that id 1 didn't have a buddy
    global user_1_state, user_1_ID
    #GPIO.output(USER1LED,False)
    user_1_state= 0
    user_1_ID= 0
    #noBuddyAPICall()
    
def SessionEnded():#enables user welcome message and disables start message
    global gui_state
    gui_state =0
    #SessionEndedAPICall()
    

setupGPIO()

win = Tk()

myFont = font.Font(family = 'Helvetica', size = 30, weight = 'bold')
#config column rows and col
Grid.rowconfigure(win,0, weight=1)
Grid.rowconfigure(win,1, weight=1)
Grid.rowconfigure(win,2,weight=1)
Grid.rowconfigure(win,3,weight=1)
Grid.columnconfigure(win,0,weight=1)
Grid.columnconfigure(win,1,weight=1)
 
win.title("Access Control")#window name
win.geometry('800x480')#size of window
win.configure(bg="white")
countDownText = "count"
countDown = Label(win,anchor=E,font= myFont, bg="white") #create label for countdown that goes in the thirdrow
countDown.grid(row=2,column=0, sticky="nsew")
timeLabel = Label(text=" ", fg='black', font=('Helvetica',25,'bold'), bg='white', anchor=W) #Third Row label displays text for minutes
timeLabel.grid(row=2,column=1)

#Title Label
top= Label(text="ECE Makerspace",anchor=W,font=myFont, fg="white", bg="red") #displays ECE makerspace in the top left corner
top.grid(row=0,column=0)
clock= Label(text=" ", font=myFont, anchor=E, fg='white', bg='red')#clock in the top left corner of screen
clock.grid(row=0,column=1)

#User Name Label
welcome= Label(text=" ", anchor=CENTER, font=myFont, fg='blue', bg='white')
welcome.grid(row=1,columnspan=2)

#End Session Label
button=Label(text=" ", anchor=CENTER, font=myFont, bg='white', fg='blue')
button.grid(row=3,columnspan=2)
 
#configurePi()

disableDevice()

th1=  ID_Check_Thread("T1",1000)# declare ID_Check as thread 1 with id 1000
th2 = Read_Card_Tread("T2",2000)# declare ID_Check as thread 2 with id 2000
th1.start()
th2.start()

while True:
    if(endTime!=0):#if their is a session running which is when endTime is not equal to zero
        countdown()
        
    clock.config(text= time.strftime("%I:%M:%S"))#Prints the time on the screen

    if(gui_state==0): #initial gui state
        welcome.config(text="Swipe Card To Begin Session", fg='blue')
        countDown.config(text="")
        timeLabel.config(text="")
        if((time.localtime().tm_hour>endOfWorkingHours and time.localtime().tm_hour <=beginningOfWorkHours)):
            button.config(text="After 5 PM, Buddy Swipe Required")
    elif(gui_state==1): #Authorized state moves it to the running state afterward
        button.config(text=" ")
        if(gui_flag==0):
            gui_count=time.time()+1
            gui_flag=1
            welcome.config(text="AUTHORIZED", fg='green')
        else:
            if(time.time()>=gui_count):
                gui_flag=0
                gui_count=0
                if(buddySwipeReuiredBy!=0):
                    gui_state=4
                else:
                    gui_state=3
    elif(gui_state==2):#Non authorized label
        button.config(text=" ")
        welcome.config(text="NOT AUTHORIZED", fg='red')
        if(gui_flag==0):
            gui_count=time.time()+1
            gui_flag=1
        else:
            if(time.time()>=gui_count):
                gui_state=0
                gui_flag=0
                gui_count=0
    elif(gui_state==3):#Running Labels  
        timeLabel.config(text="Minutes Remaining")
        if(userName != ""):
            welcome.config(text="Welcome: "+ userName, fg='blue')
        else:
            welcome.config(text="Welcome USER!", fg='blue')

        if((endTime-time.time())<=40):
            button.config(text="Reswipe To Continue Session", fg='red')
        else:
            button.config(text="Hold Button To End Session", fg='purple')
    elif(gui_state==4): #Buddy Required Label
        currentTime =buddySwipeReuiredBy-time.time() 
        if(currentTime >0):
            #print you have blank time to swipe
            print("Time for Buddy Swipe: "+str(int(currentTime/60)) +":" +str("{:02d}".format(int(currentTime%60))))
            welcome.config(text="Buddy Required, Swipe Another ID: "+str(int(currentTime/60)) +":" +str("{:02d}".format(int(currentTime%60))), fg='blue')
        else:
            buddySwipeReuiredBy=0
            noBuddySwipe()
    
    # if(GPIO.input(BUTTON2)==GPIO.LOW):
    #     print("Button 2")
    #     time.sleep(2)
    #     if(GPIO.input(BUTTON2)==GPIO.LOW):
    #         disableDevice()
    # if(GPIO.input(BUTTON1)==GPIO.LOW):
    #     print("Button 1")
    #     disableDevice()
        
                
    
    win.update()
    time.sleep(.5)  #sleeps for 1/2 a second 

win.destroy()
print("Exit")