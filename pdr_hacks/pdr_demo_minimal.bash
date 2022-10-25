#!/bin/bash

for i in {1..4}; do
	echo $i > /sys/class/gpio/export
	echo "out" > /sys/class/gpio/gpio$i/direction
	echo "0" > /sys/class/gpio/gpio$i/value
done

state=0
echo "1" > /sys/class/gpio/gpio4/value

/home/project13/bin/get_scanner.py |
	{
		while read card; do
			echo $card
			if (( $state == 0 )); then
				if (( $(cat /sys/class/gpio/gpio1/value) == 0)); then
					echo "1" > /sys/class/gpio/gpio1/value
					echo "One Swipe"
				else
					echo "1" > /sys/class/gpio/gpio2/value
					echo "1" > /sys/class/gpio/gpio3/value
					state=1
					echo "Two Swipes"
				fi
			else
				for i in {1..3}; do
					echo "0" > /sys/class/gpio/gpio$i/value
				done
				echo "Deactivated"
			fi
		done
	}
