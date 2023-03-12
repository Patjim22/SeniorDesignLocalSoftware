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
endTime=0
countDownMinutes=1
countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is


     


def exitProgram():
	print("Exit Button pressed")
	#GPIO.cleanup()
	win.quit()	
 
def countdown(): #does the countdown when it is required
    global endTime
    currentTime =endTime-time.time()                            #measures the endtime vs current time
    #currentTime = time.time()
    if(currentTime >0):
        countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)))
    else:
        endTime =0
	
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
Grid.columnconfigure(win,1,weight=1)
 
win.title("Access Control")#window name
win.geometry('800x480')#size of window
win.configure(bg='white')
countDownText = "count"
countDown = Label(win,text= countDownText ,anchor=E,font= myFont, fg="white", bg="red") #create label for countdown
countDown.grid(row=0,column=1)

#Title Label
top= Label(text="ECE Makerspace",anchor=E,font=myFont, fg="white", bg="red")
top.grid(row=0,column=0)

#User Name Label
#welcome= Label(text="Welcome USER!", anchor=CENTER, font=myFont, bg='white')
#welcome.grid(row=1,column=0)

#End Session Label
button=Label(text="Push Button To End Session", anchor=CENTER, font=myFont, bg='white', fg='blue')
#button.grid(row=3,column=0)

#Buddy Label
buddy=Label(text="Buddy Required, Swipe Another ID", anchor=CENTER, font=myFont, fg='purple', bg='white')
five=Label(text="AFTER 5PM Buddy Required", anchor=CENTER, font=myFont, bg='white', fg='red')
buddy.grid(row=3,column=0)
five.grid(row=2,column=0)

#Reswipe Label
reswipe=Label(text="Reswipe To Continue Session", anchor=CENTER, font=myFont, bg='white', fg='orange')
#reswipe.grid(row=3,column=0)

#Authorized Label
authorized=Label(text="AUTHORIZED", anchor=CENTER, font=myFont, bg='white', fg='green')
not_authorized= Label(text="NOT AUTHORIZED", anchor=CENTER, font=myFont, bg='white', fg='red')
#not_authorized.grid(row=1,column=0)

#User Name Label
welcome= Label(text="Welcome USER!", anchor=CENTER, font=myFont, bg='white')
#welcome.grid(row=1,column=0)

#Start Label
start=Label(text="Swipe Card To Begin Session", anchor=CENTER, bg='white', font=myFont, fg='blue')
start.grid(row=1,columnspan=2)




win.update()

def steptwo():
	welcome= Label(text="Welcome USER!", anchor=CENTER, font=myFont, bg='white')		
	welcome.grid(row=1,column=0)
	#countDown = Label(win,text= countDownText ,anchor=CENTER,font= myFont, bg='white')
	countDown.grid(row=2,column=0, sticky="nsew")
	button=Label(text="Push Button To End Session", anchor=CENTER, font=myFont, bg='white', fg='blue')
	button.grid(row=3,column=0)
	newstart= False

endTime = time.time()+countDownIncrementer

#main
while True:
	
		
	if time.time() <= endTime:
		countdown()
	else: countDown.config(text= time.strftime("%I:%M:%S"))
	time.sleep(10)
	buddy.grid_forget()
	five.grid_forget()
	win.update()



