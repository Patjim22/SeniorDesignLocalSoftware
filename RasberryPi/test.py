import sys
import re


for line in sys.stdin:
    if  'q' == line.rstrip():
        break
    regSearch =re.compile('\+.*')
    cardNumber = regSearch.match(line)
    #print(cardNumber)
    if(cardNumber!=None):
        #print(cardNumber.group()[1:10])
        print()
    else:
        print(len(line))
        if(len(line)==10):
            print(line[0:8])
    
    #print(line)
    
