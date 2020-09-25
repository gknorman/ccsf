#!/usr/local/bin/env python3
#
# Date: 09/20/20
# Course: CS 231 - Advanced Python
# Prof: Aaron Brick
# Term: Fall 2020
#
# Assignment #4
# Description:  Write a program to lazily rewrap text from the filename 
# passed so that it fits an 80 column window without breaking any words.

import sys


def lazyReader(aFile):
	for block in aFile.readlines():
		yield block

def getWords(aBlock):
	for word in aBlock.split():
		yield word


def processFiles(arg):
	try:
		# Open the file using a file object wrapper, and name the object 'file'
		with open(arg) as file:

			print("*" * 80)
			print("Reading from: " + file.name)
			print("*" * 80)

			# I know this isn't very functional... I couldn't figure out in time how to do this without 
			# doing a bunch of manual temp data swaps and state management.... 
			current_line = []
			temp_line = []

			# Call the generator function to get the next 'line' of text
			for block in lazyReader(file):

				# Check if the current line of text is too short
				# If it is, add it to temp and skip to the next iteration of the for loop
				if len(block.strip()) + len(" ".join(temp_line)) < 80:
					temp_line += block.split()
					continue

				# Otherwise, if there's data in temp_line, remove it and add it to current_line
				if len(temp_line) > 0:
					current_line += temp_line
					temp_line = []

				# Pass the next line of text from 'file' to a function that yields words from the line
				for word in getWords(block):

					# Add words from the generator function, getWords, until the 
					# length of current_line is just under 80 characters
					if len(" ".join(current_line) + " " + str(word)) < 80:
						current_line.append(word)
					else:
						# If there's remaining words in the block, add them to temp_line for the next iteration
						temp_line.append(word)

				# Uncomment this line to print the character count before the line
				# print(str(len(" ".join(current_line))) + " : " + " ".join(current_line))
				# print(" ".join(current_line))
				yield " ".join(current_line)
				current_line = []
			if len(temp_line) > 0:
				# Uncomment this line to print the character count before the line
				# print(str(len(" ".join(temp_line))) + " : " + " ".join(temp_line))
				# print(" ".join(temp_line))
				yield " ".join(temp_line)

	except FileNotFoundError:
		print ('File not found.' )
	except PermissionError:
		print ('File not readable.' )
	except IsADirectoryError:
		print ('File is a directory.' )


# This is the driver of the program; It checks whether or not command line arguments have
# been provided by the user, of if the program should read urantia.txt from the instructor's filepath
def main():	
	if len(sys.argv[1:]) > 0:
		for line in processFiles(sys.argv[1]):
			print(line)
	else:
		print("*" * 80)
		print("No filepath given to program.")
		print("Reading default filepath: /users/abrick/resources/urantia.txt")
		print("*" * 80)
		for line in processFiles('/users/abrick/resources/urantia.txt'):
			print(line)
# Execute the main function
main()

# EOF