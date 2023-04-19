# Makerspace Access Control
This repository contains the python programs that run on the rasberry pi to control the machines and check against a Database via an API. 

# Dependencies
This program Requires a display environment to function
* Python libraries
  * threading
  * tkinter RPi.GPIO
  * evdev
  * sql_connection
  * json
  * os
  * re
Requires Python's hook with mariadb (pip install mariadb)

The Program that reads keycards and interpruts what to do is in MainProgram.py. 
sql_connection.py holds all API call functions.

Run_Program.bash is a script to execute MainProgram.py to start it running
