import threading
import time
import sys
import re
from tkinter import *
from tkinter import font


card = "0"
global start 
global endTime
global countDownText
countDownMinutes=1
endOfWorkingHours=17	#5pm
beginningOfWorkHours=8	#8am
user_1_state = 0
user_2_state = 0

countDownIncrementer = countDownMinutes*60 #number of minutes wanted goes where the 1 is


class myThread1 (threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID

    # helper function to execute the threads
    def run(self):
        global T1
        global T2
        while True:

            if("22"== card):
                T1= False
                T2= False
                print("ExitT1")
                break
            
            time.sleep(1)

class ReadCardTread (threading.Thread):
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
                    print(line[0:8])
            time.sleep(10)
            
def countdown():
	#currentTime =endTime-time.time()
    currentTime = time.time()
	#print(int(currentTime/60),":", int(currentTime%60))
    countDown.config(text=str(int(currentTime/60)) +":" +str(int(currentTime%60)))
	#countDown.config(text=str(int(currentTime))+":")
	#print(str(time.localtime().tm_hour) +":"+str(time.localtime().tm_min))
	
	
	#time.sleep(1)
    win.update()
	



T1 = True
T2 = True
    
        



th1=  myThread1("T1",1000)
th2 = ReadCardTread("T2",4000)



th1.start()
th2.start()

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


ledButton = Button(win, text = "LED ON", font = myFont, height = 2, width =8 )
ledButton.grid(row=1)
#ledButton.pack()
#if( (int(time.ctime(time.time()))>=17 )and (int(time.ctime(time.time()))<=8) ):
	#print(time.ctime(time.time()))
endTime = time.time()+countDownIncrementer


while T1:
    countdown()
    #if(input().rstrip()=="q"):
    #    T1 = False
    #   T2 = False
    #    break
    #print("Hello " +str(T1))
    time.sleep(.5)   

win.destroy()
print("Exit")