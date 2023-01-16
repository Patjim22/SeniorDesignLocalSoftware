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






def exitProgram():
	print("Exit Button pressed")
	#GPIO.cleanup()
	win.quit()	
 
def countdown():
	currentTime =endTime-time.time()
	#print(int(currentTime/60),":", int(currentTime%60))
	countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)) +" minutes remaining")
	#countDown.config(text=str(int(currentTime))+":")
	#print(str(time.localtime().tm_hour) +":"+str(time.localtime().tm_min))
	
	
	#time.sleep(1)
	win.update()
	
def configurePi():
    #pull config data from SQL database
    return

    

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
exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =2 , width = 6) 
#exitButton.pack(side = BOTTOM)

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

#Reswipe Label

#Authorized Label

#Start Label


endTime = time.time()+countDownIncrementer


 
while True:
    if time.time() <= endTime:
      countdown()



