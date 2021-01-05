#!/usr/bin/env python
'''
Date: 11/08/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

Assignment #11 - CPython

Description:  Write a universal launcher program
that expects its command line arguments to contain
the absolute path to a program in any language,
followed by its arguments.

The wrapper should transparently run that program
and exit with its exit value.
'''

import sys
import subprocess

def runProcess(arguments):
    result = subprocess.run(arguments, stdout=subprocess.PIPE, text=True)
    print("\nPrinting STDOUT for: " + f"{result.args}" + "\n")
    print("-" * 80)
    print(result.stdout)
    print("-" * 80)
    print("\nExecuted with RETURN CODE: " + f"{result.returncode}" + "\n")

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("No commands passed to program at Command Line!")
        print("Using default command of 'ls -al'")
        runProcess(['ls','-la'])
    else:
        commands = sys.argv[1:]
        print(commands)
        runProcess(commands)


