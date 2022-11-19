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


win = Tk()

myFont = font.Font(family = 'Helvetica', size = 36, weight = 'bold')


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
 
 
win.title("First GUI")
win.geometry('800x480')
countDownText = "count"
countDown = Label(win,text= countDownText ,anchor=CENTER,font= myFont)
countDown.pack()

exitButton  = Button(win, text = "Exit", font = myFont, command = exitProgram, height =2 , width = 6) 
exitButton.pack(side = BOTTOM)

ledButton = Button(win, text = "LED ON", font = myFont, command = ledON, height = 2, width =8 )
ledButton.pack()
#if( (int(time.ctime(time.time()))>=17 )and (int(time.ctime(time.time()))<=8) ):
	#print(time.ctime(time.time()))
endTime = time.time()+20

def countdown():
	currentTime =endTime-time.time()	
	#print(int(currentTime/60),":", int(currentTime%60))
	countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)))
	
	#time.sleep(1)
	win.update()
	win.after(1000,)

while(time.time() <= endTime):
	countdown()


