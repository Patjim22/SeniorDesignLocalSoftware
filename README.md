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

# Image Build Tool (build.bash)

* Run `build.bash` to create an image, tagged with the build date.
	* Requires root access
	* No arguments needed, the image name is 
