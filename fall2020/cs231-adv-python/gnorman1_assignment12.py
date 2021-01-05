#!/usr/bin/env python
'''
Date: 11/15/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

Assignment #12 - Concurrency

 Write a program that creates a pool of workers
 to all at once check whether or not the files whose
 pathnames are passed in are encoded in UTF-8
'''
import concurrent.futures
import codecs
import sys
import time
from threading import current_thread
from datetime import datetime
import threading
import logging


def check_if_utf(path):
    try:
        startTime = time.perf_counter()
        threadName = current_thread().name
        line = codecs.open(path, encoding="utf-8", errors="strict").readline()
        return [threadName, startTime, f"UTF-8 encoded: {path}"]
    except UnicodeDecodeError:
        return [threadName, startTime,  f"-- Warning: {path} is NOT utf-8 encoded"]
    except IsADirectoryError:
        return [threadName, startTime, f"-- Warning: {path} is NOT utf-8 encoded, it's a Directory!"]
    except PermissionError:
        return [threadName, startTime, f"-- ERROR [Errno 13]: Permission denied: {path}"]
    except FileNotFoundError:
        return [threadName, startTime, f"-- ERROR [Errno 2]: File Not Found: {path}"]


def main():
    with concurrent.futures.ThreadPoolExecutor(thread_name_prefix='thread') as executor:

        futures = []

        # Parse the filename paths given as args on the command line
        for filename in sys.argv[1:]:
            futures.append(executor.submit(check_if_utf, path=filename))

        # Print the results of check_if_utf() as they are executed
        for future in concurrent.futures.as_completed(futures):
            # Store list of values returned by .result()
            result = future.result()

            # [0] has the Thread#, [1] has the Start Time, [2] says whether it's utf-8 or not
            print(result[2])
            print(f"\tTime on {result[0]}: {time.perf_counter() - result[1]:.3f} seconds\n")

        # Alternate usage of executor.map() but this causes all tasks to be done in order
        # futures = executor.map(check_if_utf, list(sys.argv[1:]))
        # for future in futures:
        #     print(future)

if __name__ == '__main__':
    # Use the following line instead of main() to get performance timing
    # cProfile.run('main()')
    starttime = time.perf_counter()
    # print(f"Starting main() at: {datetime.now().strftime('%H:%M:%S')}")
    main()
    endtime = time.perf_counter()
    print(f"Program took: {endtime-starttime:.3f} total seconds to complete!")
