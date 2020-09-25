#!/usr/local/bin/env python3
#
# Date: 09/27/20
# Course: CS 231 - Advanced Python
# Prof: Aaron Brick
# Term: Fall 2020
#
# Assignment #5
# Description:  Demonstrate the use of a generator that indicates 
# for each event in access_log the number of seconds elapsed since 
# the most recent midnight

import sys
from datetime import datetime

# storing path to access log as per Prof. Brick's notes
log = '/etc/httpd/logs/access_log'

# storing generator here, but keeping only the slice of the 4th element
# which represent the timestamps in the log.
# process it up front into a hh:mm:ss string
generator = (":".join(line.split()[3].split(":")[1:]) for line in open(log))

# Function that gets the number of seconds since previous midnight
# as a datetime "timedelta" object
def dateDiffSeconds(dateString):
	timeformat = '%H:%M:%S'
	date2 = datetime.strptime('00:00:00',timeformat)
	date1 = datetime.strptime(dateString,timeformat)
	return (date1 - date2).seconds

# prints the seconds returned from above function a default of 10 times.
def printEntries(x=10):
	for i in range(x):
		seconds = dateDiffSeconds(next(generator))
		print(f"#{i + 1}: {seconds} seconds")

# if the program is run without any input at the command line, eg. program.py
# then program executes first block, since lenght of sys.argv is less than 2 
# (the first element in sys.argv is the name of the program).
if len(sys.argv) < 2:
	print("*" * 30 + "\n")
	print("Current Usage: Printing seconds from previous midnight per entry" + "\n" + \
		"for 10 Entries from /etc/httpd/logs/access_log" + "\n")
	print("*" * 30 + "\n")
	
	try:
		# Call to function with default argument of 10
		printEntries()

		print("\n" + "*" * 30)

		print("\n" + "Alternative Usage: Pass an integer at the command line to " + "\n" + \
			"change the number of times this program yields a timestamp" + "\n")

		print("eg. python3 this_program.py 20" + "\n")
	
	except Exception as e:
		print("Please only pass a single integer to the program at the command line")

# if arguments were passed to the program at the command line, this else block will execute
else:
	try:
		print("*" * 30 + "\n")
		# prints the integer passed at the command line using f-string and the sys.argv[] array.
		# the user's argument should be the 2nd element in the array
		print("Current Usage: Printing seconds from previous midnight per entry" + "\n" + \
			f"for {sys.argv[1]} Entries from /etc/httpd/logs/access_log" + "\n")

		print("*" * 30 + "\n")

		# Call printEntries the number of times passed at the command line
		printEntries(abs(int(sys.argv[1])))

		print("\n" + "*" * 30 + "\n")
	
	# catch all exception is raised if there's any issues with the user's argument passed at the command line
	except Exception as e:
		
		print("Please only pass a single integer to the program at the command line")

