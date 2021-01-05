#!/usr/local/bin/env python3
#
# Date: 10/17/20
# Course: CS 231 - Advanced Python
# Prof: Aaron Brick
# Term: Fall 2020
#
# Assignment #8 - Decorators
# Description:  Decorate print() such that
# (A) it refuses to print anything under ten characters
# long and (B) only five calls are allowed.

import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        # Updating nums_calls has to come before the return
        # statements or it won't be executed!
        wrapper_count_calls.num_calls += 1
        # changed len(*args) to len(" ".join(args)) to accept multiple args to print()
        if(wrapper_count_calls.num_calls < 6 and len(" ".join(args)) >= 10):
                return func(*args, **kwargs)
    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls

# Using assignment method to apply decorator
# to the standard built-in print()
print = count_calls(print)

if __name__ == '__main__':
    print("Call 1 - This can print, it's at least 10 chars long.\n")
    print("Call 2 ??","lkdsjf")
    print("Call 3 - This can print, but Call 2 was too short!")
    print("Call 4 - This can print too.")
    print("Call 5 - This can print, but nothing will print after this!")
    print("Call 6 - This won't print, it's over the 5 call limit")
    print("Call 7 - This can't print either")
