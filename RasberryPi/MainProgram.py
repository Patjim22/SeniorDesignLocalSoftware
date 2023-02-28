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
twoSwipeTime = 20        #used to hold how long to wait for a buddy to swipe
buddySwipeReuiredBy=0   #holds the time to cancel out and say you were rejected because no buddy
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
BUZZER = 18
BUTTON1 = 5
BUTTON2 = 6

BackUp_USER= {"200248706", "200289830"}
channel_list = (5,6,9,11,13,14,15,17,18,19,26)              



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
                if(endTime==0):                         #if endtime ==0 then no one is currently using the machine
                    assignUserToMachine(card)
                else:
                    if((user_1_ID ==card) or (user_2_ID ==card)):
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
        disableDevice()
	
def configurePi():#pull config data from SQL database
    countDownMinutes # should be editable to change the length of the countdown
    endOfWorkingHours # changes the end time of the makerspace working hours
    beginningOfWorkHours # changes the start time of the makerspace working hours
    twoSwipeTime #deault is 10sec change to give buddy more or less time to swipe after first swipe
    return

def enableDevice(): #enables the usb and Control OPTO issolators and starts the countdown
    global endTime
    #GPIO.output(CONTROLOPTO,True)              # Opto
	#GPIO.output(USBSEL,True)                 	# USB
    print("ACTIVATED")
    #GPIO.output(DEVICEON,True)                	# Device enable light
    endTime = time.time()+countDownIncrementer

def disableDevice():
    global user_1_state , user_2_state,user_2_ID, user_1_ID, endTime, userName
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
    userName =""
    
    endTime=0

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

def assignUserToMachine(card):
    global user_1_state , user_2_state, user_1_ID, user_2_ID, buddySwipeReuiredBy
    authorized = check_if_authorized(card)
    if(authorized):
        if(user_1_state==0):
            user_1_state=1
            user_1_ID= card
        if(user_1_state==1):
            if(card != user_1_ID):
                user_2_state=1
                user_2_ID = card
                buddySwipeReuiredBy=0
        if(time.localtime().tm_hour<endOfWorkingHours and time.localtime().tm_hour >=beginningOfWorkHours):#during working houres only 1 user is needed
            if(user_1_state or user_2_state):
                enableDevice()     
        else:#outside of normal hours a buddy is required
            if(user_1_state and user_2_state):
                enableDevice()
            else:
                print("A buddy is required")        #needs to write to a label on the gui
                buddySwipeReuiredBy=time.time()+twoSwipeTime     
    else:
        print("non-authorized user")

def noBuddySwipe():#send to database that id 1 didn't have a buddy
    user_1_ID
    
T1 = True
T2 = True

win = Tk()

myFont = font.Font(family = 'Helvetica', size = 30, weight = 'bold')
#config column rows and col
Grid.rowconfigure(win,0, weight=1)
Grid.rowconfigure(win,1, weight=1)
Grid.rowconfigure(win,2,weight=1)
Grid.rowconfigure(win,3,weight=1)
Grid.columnconfigure(win,0,weight=1)
 
win.title("Access Control")#window name
win.geometry('800x480')#size of window
countDownText = "count"
countDown = Label(win,text= countDownText ,anchor=CENTER,font= myFont, bg="white") #create label for countdown
#countDown.pack()
countDown.grid(row=2,column=0, sticky="nsew")#puts the countdown to the center of the screen


#Title Label
top= Label(text="ECE Makerspace",anchor=E,font=myFont, fg="white", bg="red")
top.grid(row=0,column=0)

#User Name Label
welcome= Label(text="Welcome USER!", anchor=CENTER, font=myFont, bg="white")
welcome.grid(row=1,column=0)

#End Session Label
button=Label(text="Push Button To End Session", anchor=CENTER, font=myFont, bg="white")
button.grid(row=3,column=0)

#Buddy Label
buddy=Label(text="Buddy Required, Swipe Another ID", anchor=CENTER, font=myFont, bg='white')

#Reswipe Label
reswipe=Label(text="Reswipe To Continue Session", anchor=CENTER, font=myFont, bg='white', fg='red')

#Authorized Label
#authorized=Label(text="AUTHORIZED", anchor=CENTER, font=myFont, bg='white', fg='green')
#not_authorized= Label(text="NOT AUTHORIZED", anchor=CENTER, font=myFont, bg='white', fg='red')

#User Name Label
#welcome= Label(text="Welcome USER!", anchor=CENTER, font=myFont, bg='white')

#Start Label
#start=Label(text="Swipe Card To Begin Session", anchor=CENTER, bg='white', font=myFont, fg='blue')

   
    
configurePi()

disableDevice()

countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is
th1=  ID_Check_Thread("T1",1000)
th2 = Read_Card_Tread("T2",2000)
th1.start()
th2.start()

while T1:
    if(endTime!=0):
        countdown()
    else:
        countDown.config(text= time.strftime("%I:%M:%S")) #displays time in 12 hour format
    
    if(buddySwipeReuiredBy!=0):
        currentTime =buddySwipeReuiredBy-time.time() 
        if(currentTime >0):
            #print you have blank time to swipe
            countDown.config(text="Time for Buddy Swipe: "+str(int(currentTime/60)) +":" +str(int(currentTime%60)))
        else:
            buddySwipeReuiredBy=0
            noBuddySwipe()
            
    if(userName != ""):
        welcome.config(text="Welcome: "+ userName)
    else:
        welcome.config(text="Welcome USER!")
    
    win.update()
    time.sleep(.5)  #sleeps for 1/2 a second 

win.destroy()
print("Exit")