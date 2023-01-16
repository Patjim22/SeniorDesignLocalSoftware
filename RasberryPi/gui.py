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
countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is





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



