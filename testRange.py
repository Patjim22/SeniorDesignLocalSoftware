TIMESTOBUZ = {5,2,1,.33}
TIMETOTURNBUZZERON =10


for currentTime in range(0,5*60):
    buzzEnable = False
    for value in TIMESTOBUZ:
            
            if(currentTime <= value*60 and currentTime >= value*60 - TIMETOTURNBUZZERON):
                #GPIO.output(BUZZER,True)
                print("Buzz")
                buzzEnable = True
                
    if buzzEnable == False:
        print("OFF")       