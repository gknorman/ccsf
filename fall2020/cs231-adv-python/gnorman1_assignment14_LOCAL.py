#!/usr/bin/env python
"""
Date: 11/29/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

Assignment #14 - Feature extraction

 Write a program that expects as argument the path to a greyscale
 ASCII PGM file, and prints out a sixteeen-bucket histogram
 counting the pixels at each level of grey.
"""
import collections
import math
import sys
import re
import traceback
from collections import OrderedDict, Counter


# Trying out a custom exception to handle non-pgm files
# Used this tutorial:
# https://www.datacamp.com/community/tutorials/exception-handling-python
class WrongFileType(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return repr(self.data)


# Uses Prof. Brick's example to open and list all of the
# greyscale values for each pixel in the pgm file
def openpgm(path_to_file):
    try:
        if path_to_file.split(".")[-1] != "pgm":
            raise WrongFileType(f"{path_to_file}")
        else:
            with open(path_to_file) as content:
                parts = re.split(r'\s+', re.sub(r'#.*', r'\n', content.read()))
                x_dim, y_dim, depth = int(parts[1]), int(parts[2]), int(parts[3])
                pixels = [int(n) for n in parts[4:] if n]
                assert len(pixels) == x_dim * y_dim
                FACTOR = 3
                two_d = collections.defaultdict(dict)
                for y in range(y_dim):
                    for x in range(x_dim):
                        two_d[x][y] = pixels[x + x_dim * y]
                # Create a simple upscaling using nearest-neighbor sampling.
                header = 'P2\n{} {}\n{}\n'.format(x_dim * FACTOR, y_dim * FACTOR, depth)
                with open('larger.pgm', 'w') as larger:
                    larger.write(header)
                    for y in range(y_dim * FACTOR):
                        for x in range(x_dim * FACTOR):
                            larger.write((str(two_d[x // FACTOR][y // FACTOR]) + ' '))
            return pixels
    except WrongFileType as e:
        print("ERROR: This program can only handle .pgm files.")
        print("Program received this file instead: " + e.data)


# Count the frequency of each greyscale value in the image
# Note, Counter is only used as a sanity check,
# but since it doesn't order it's keys I was afraid to stick
# with it during later steps.
def countgreyvals(pixels):
    count_per_grey_value = OrderedDict()
    for i in sorted(pixels):
        count_per_grey_value[i] = count_per_grey_value.get(i, 0) + 1
    b = Counter(sorted(pixels))
    assert b == count_per_grey_value
    return count_per_grey_value


# Doesn't do much except create a list of intervals
# that define and label the 16 buckets of the histogram
def generatelabels():
    a = 0
    b = 0
    labels = []
    for i in range(1, 17):
        a = 0 if i == 1 else b + 1
        b = i * 16 - 1
        labels.append([a, b])
    return labels


# Sums up the frequencies of the greyscale values by bucket
# that the greyscale value fits into.
def populateintervals(count_per_grey_value, count_per_bucket, labels):
    for k, v in count_per_grey_value.items():
        for key, interval in zip(enumerate(labels), labels):
            if interval[0] < k <= interval[1]:
                # print(key[0], interval[0], k, v, interval[1])
                count_per_bucket[key[0]] = count_per_bucket.get(key[0], 0) + v
    return count_per_bucket


# Finally prints the histogram using the bucket labels and
# summed frequencies per greyscale range.
def printhistogram(labels, count_per_bucket):
    print("Greyscale Ranges", "\t", "Count of Pixels per Range")
    print("-" * len("Greyscale Ranges"), "\t", "-" * len("Count of Pixels per Range"))
    for label, bar in zip(labels, count_per_bucket.values()):
        # Thank you Kenneth Sy for posting the character '█' in
        # the forum to print this better looking histogram!
        print(label, "\t\t|", '█' * math.ceil(bar / 900), bar)



if __name__ == '__main__':
    # These variables only need to be initialized once
    count_per_range_of_greys = OrderedDict({i: 0 for i in range(0, 16)})
    labels = generatelabels()

    # Default execution if no pgm files provided at command line
    if len(sys.argv[1:]) < 1:
        print("*" * 80)
        print("No file provided via command line" + "\n")
        print("Generating Histogram with default file: ")
        print("/users/abrick/resources/maquinna.pgm")
        print("-" * 80, "\n")

        pixels = openpgm("maquinna.pgm")
        count_of_greys = countgreyvals(pixels)
        count_per_range_of_greys = populateintervals(count_of_greys, count_per_range_of_greys, labels)
        printhistogram(labels, count_per_range_of_greys)

        print("_" * 80)

    else:
        for file in sys.argv[1:]:
            try:
                print("*" * 80, "\n")
                print("Generating Histogram for file: " + f"{file}")
                print("-" * 80, "\n")

                # Calls the main 4 functions

                # Get the list of all greyscale values in the image
                pixels = openpgm(file)

                # Count the frequency each greyscale value
                count_of_greys = countgreyvals(pixels)

                # Sum the frequencies per interval of greyscale values
                # to generate a 16-interval histogram
                count_per_range_of_greys = populateintervals(count_of_greys, count_per_range_of_greys, labels)

                # Lastly, print the historgram
                printhistogram(labels, count_per_range_of_greys)

                print("_" * 80)
            except Exception as e:
                print(e)
                tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
                print("".join(tb_str))
