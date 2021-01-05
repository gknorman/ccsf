#!/usr/bin/env python
"""
Date: 12/06/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

 Assignment #15 - Translation

 Modify last week's program to also write an output
 PGM file with higher contrast, displaying grey
 level histograms for both the input and the output
"""
import traceback
from math import ceil
import collections
import sys
import re


def countgreyvals(pixels, depth):
    pixl_counts = [0 for _ in range(depth + 1)]
    for n in pixels:
        pixl_counts[n] += 1
    return pixl_counts


def openpgm(path_to_file):
    if path_to_file.split(".")[-1] != "pgm":
        print(f"Can't open non-pgm files" + "\n" +
              f"Error opening:{path_to_file}")
    else:
        with open(path_to_file) as content:
            parts = re.split(r'\s+', re.sub(r'#.*', r'\n', content.read()))
            x_dim, y_dim, depth = int(parts[1]), int(parts[2]), int(parts[3])
            pixels = [int(n) for n in parts[4:] if n]
            header = 'P2\n{} {}\n{}\n'.format(x_dim, y_dim, depth)

    return path_to_file, header, x_dim, y_dim, depth, pixels


def create_histogram(path_to_file, depth, pixels):
    # All credit goes to /users/abrick/pr/231/2656/rw.py
    # for showing a much more pythonic way of creating the histogram below:
    bin_size = 16
    pixl_counts = countgreyvals(pixels, depth)
    bin_counts = [sum(pixl_counts[i:i + bin_size])
                  for i in range(0, depth + 1, bin_size)]

    # Apparently using :, inside of an f-string can format numbers so that
    # they have commas in between the numbers.
    bin_label = [f'({x:,})' for x in bin_counts]

    # This creates the text that labels each column, x to x+15
    # for our greyscale files, bin_size will be 16,
    # and depth will be 256.
    labels = [f'[{i}-{i + bin_size - 1}]'
              for i in range(0, depth + 1, bin_size)]

    # Thank you Kenneth Sy for posting the character '█' in
    # the forum to print this better looking histogram!

    # As /users/abrick/pr/231/2656/rw.py shows, we can adjust the size of the
    # histogram height to fit in the terminal:
    plot = ['█' * ceil(60 * (n / max(bin_counts)))
            for n in bin_counts]

    # print(ceil(70 * n / (max(bin_counts) + len(f'{max(bin_counts)}')) for n in bin_counts))

    hist = "\n".join(f'{x:}'.ljust(18) + f'{y} {z}'
                     for x, y, z in zip(labels, plot, bin_label))

    title = f'Histogram for file: {path_to_file}\n'

    tablen = max(round((90 - len(title)) / 2), 0)
    title = f'\t{title}\n'.expandtabs(tablen)
    legend = 'Gray Values \tBin Counts\n'.expandtabs(6)
    hist = f'{title}{legend}{hist}'

    return hist


def adjust_contrast(path_to_file, header, x_dim, y_dim, depth, pixels, amount):
    factor = (259 * (amount + 255)) / (255 * (259 - amount))
    factor = factor if factor > 0 else 1

    # reduced_contrast_pixels = [min(max(round(factor * pixel), 0),255)
    #                            if pixel < (depth / 2.0)
    #                            else min(round(pixel / factor), 255)
    #                            for pixel in pixels]

    increased_contrast_pixels = [min(max(round(pixel / factor), 0), 255)
                                 if pixel < (depth / 2.0)
                                 else min(round(pixel * factor), 255)
                                 for pixel in pixels]

    two_d = collections.defaultdict(dict)
    for y in range(y_dim):
        for x in range(x_dim):
            two_d[x][y] = increased_contrast_pixels[x + x_dim * y]

    path_to_file = (path_to_file.split("/")[-1]).split(".")[0]
    path_to_file = f'{path_to_file}' + "_contrast_changed"

    with open(f'{path_to_file}.pgm', 'w') as adjusted:
        print("\nSaving new file..\n")
        adjusted.write(header)
        for y in range(y_dim):
            for x in range(x_dim):
                adjusted.write((str(two_d[x][y]) + ' '))

    return path_to_file, depth, increased_contrast_pixels


if __name__ == '__main__':
    # Default execution if no pgm files provided at command line
    if len(sys.argv[1:]) < 1:
        print("*" * 80)
        print("No file provided via command line" + "\n")
        print("Generating Histogram with default file: ")
        print("/users/abrick/resources/maquinna.pgm")
        print("-" * 80, "\n")

        path_to_file, header, x_dim, y_dim, depth, pixels \
            = openpgm("/users/abrick/resources/maquinna.pgm")

        print(create_histogram(path_to_file, depth, pixels))

        print("-" * 80, "\n")

        change_contrast_amount = 20
        adjusted_path_to_file, depth, new_pixels \
            = adjust_contrast(path_to_file, header,
                              x_dim, y_dim, depth, pixels,
                              change_contrast_amount)

        print(create_histogram(adjusted_path_to_file, depth, new_pixels))
        print("_" * 80)

    else:
        print("USAGE: add \'f\' or \'-f\' followed by an integer greater than 0")
        print("\t to change the contrast adjustment amount")
        if sys.argv[1] == "f" or sys.argv[1] == "-f":
            change_contrast_amount = int(sys.argv[2])
            start = 3
        else:
            change_contrast_amount = 20
            start = 1

        for file in sys.argv[start:]:
            try:
                print("*" * 80, "\n")
                print("Generating Histogram for file: " + f"{file}")
                print("-" * 80, "\n")

                path_to_file, header, x_dim, y_dim, depth, pixels \
                    = openpgm(f"{file}")
                print(create_histogram(path_to_file, depth, pixels))
                print("-" * 80, "\n")

                adjusted_path_to_file, depth, new_pixels \
                    = adjust_contrast(path_to_file, header,
                                      x_dim, y_dim, depth, pixels,
                                      change_contrast_amount)

                print(create_histogram(adjusted_path_to_file, depth, new_pixels))
                print("_" * 80)
            except Exception as e:
                print(e)
                tb_str = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
                print("".join(tb_str))
