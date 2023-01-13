import sys


for line in sys.stdin:
    if  'q' == line.rstrip():
        break
    print(line[1:16])
print("Exit")