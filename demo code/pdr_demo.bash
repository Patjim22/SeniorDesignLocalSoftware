#!/bin/bash

# Initialize all pins to OUT OFF
arr=(2 3 4 17 27 14)
for i in ${arr[@]}; do
	echo $i > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio$i/direction
	echo "0" > /sys/class/gpio/gpio$i/value
done

# Define constants and variables

USER_1=200338060
USER_2=200248706

user_1_state=0
user_2_state=0

# Set power pin to on
echo "1" > /sys/class/gpio/gpio27/value
# Set switch pin to default
echo "1" > /sys/class/gpio/gpio3/value

# Give scanner time to get online

echo "INITIALIZED"

# Pipe scanner input to subshell
./get_scanner.py |
	{
		while read card; do
			# Register cards read
			echo $card

			# Check for user 1
			if (( $user_1_state == 0 )) && [[ $card == $USER_1 ]]; then
				echo "1" > /sys/class/gpio/gpio4/value
				user_1_state=1
				echo 'USER 1'
			fi

			# Check for user 2
			if (( $user_2_state == 0 )) && [[ $card == $USER_2 ]]; then
				echo "1" > /sys/class/gpio/gpio17/value
		 		user_2_state=1
				echo 'USER 2'
			fi

			# Activate if both users logged in
			if (( $user_2_state == 1 )); then
				echo "1" > /sys/class/gpio/gpio2/value
				echo "0" > /sys/class/gpio/gpio3/value
				echo 'ACTIVATED'
				echo "1" > /sys/class/gpio/gpio14/value #enable usb switch
			fi

			# Deactivate and cancel auth if user invalid
			if [[ $card != $USER_1 ]] && [[ $card != $USER_2 ]]; then
				echo "0" > /sys/class/gpio/gpio2/value
				echo "1" > /sys/class/gpio/gpio3/value
				pins_off=(4 17 14) #disable usb, machine, and active user leds
				for i in ${pins_off[@]}; do
					echo "0" > /sys/class/gpio/gpio$i/value
				done
				
				user_1_state=0
				user_2_state=0
				echo 'DEACTIVATED'
			fi
		done
	}
