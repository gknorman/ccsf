#!/usr/local/bin/env python3
#
# Date: 09/13/20
# Course: CS 231 - Advanced Python
# Prof: Aaron Brick
# Term: Fall 2020
#
# Assignment #2
# Description:  Write a program that demonstrates a generator 
# yielding one timestamp at a time from /etc/httpd/logs/access_log

import sys

# storing path to access log as per Prof. Brick's notes
log = '/etc/httpd/logs/access_log'

# storing generator here, but keeping only the slice of the 4th & 5th elements
# which represent the timestamps in the log
generator = (line.split(" ")[3:5] for line in open(log))

# if the program is run without any input at the command line, eg. > program.py 10
# then program executes first block, since lenght of sys.argv is less than 2 (the first element in sys.argv is the name of the program).
if len(sys.argv) < 2:

	print("*" * 30 + "\n")
	print("Current Usage: Printing 10 timestamps from /etc/httpd/logs/access_log" + "\n")
	print("*" * 30 + "\n")
	
	# I'm paranoid about runtime exceptions while working with external files, so practicing use of try/except blocks here
	try:

		# as long as the user keeps entering the character, 'y', program will keep calling next on the generator object
		# while(str(input("Enter Y to continue, anything else to quit: ")[0]).lower() == 'y'):
		# 	print(" ".join(next(generator)))

		#  ....Apparently, the input() function violates course policies??  Scratching this interactive mode for now.

		print("\n".join(" ".join(next(generator)) for _ in range(10)))

		print("\n" + "*" * 30)
		print("\n" + "Alternative Usage: Pass an integer at the command line to change the number of times this program yields a timestamp" + "\n")
		print("eg. python3 this_program.py 20" + "\n")
	
	except Exception as e:
		# print("Please input only letters and numbers in interactive mode.")
		print("Please only pass a single integer to the program at the command line")

# if arguments were passed to the program at the command line, this else block will execute
else:

	try:

		print("*" * 30 + "\n")
		# prints the integer passed at the command line using f-string and the sys.argv[] array.
		# the user's argument should be the 2nd element in the array
		print(f"Current Usage: Printing {sys.argv[1]} timestamp(s) from /etc/httpd/logs/access_log" + "\n")

		print("*" * 30 + "\n")
		
		# if the user's arg is valid, the generator should be called that number of times
		print("\n".join(" ".join(next(generator)) for _ in range((abs(int(sys.argv[1]))))))

		print("\n" + "*" * 30 + "\n")
	
	# catch all exception is raised if there's any issues with the user's argument passed at the command line
	except Exception as e:
		
		print("Please only pass a single integer to the program at the command line")

