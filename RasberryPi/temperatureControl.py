from time import sleep, strftime, time
from gpiozero import CPUTemperature
import RPi.GPIO as GPIO

cpu = CPUTemperature()
GPIO.setmode(GPIO.BOARD)                                   #Use Board pin numbers
GPIO.setwarnings(False)                                    # Suppresses warning messages from output.
GPIO.setup(channel_list, GPIO.OUT, initial =GPIO.LOW)
with open("/home/Project13/cpu_temp.csv", "a") as log:
    while True:
        temp=cpu.temperature
        if(temp >=60):
            
        sleep(60) 