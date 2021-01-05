#!/usr/bin/env python
'''
Date: 11/22/20
Course: CS 231 - Advanced Python
Prof: Aaron Brick
Term: Fall 2020

Assignment #13 - Persistent Stores

 Write a CSV-to-JSON translator that expects a path to a
 CSV file as argument, and for each line, prints out a
 JSON object encapsulating that record.
'''

import csv
import json
import pprint
import ssl
import sys
import urllib.request
from os import path


def downloadCsvLocal(url):
    context = ssl._create_unverified_context()
    file_name = f"{(url.split('/')[-1]).split('.')[0]}.csv"
    if path.exists(file_name):
        return file_name
    else:
        with urllib.request.urlopen(url, context=context) as response, open(file_name, 'wb') as local_file:
            data = response.read()
            local_file.write(data)
        return file_name

def csvToJson(filePath):

    jsonfile = []

    if(filePath[0:4] == "http"):
        localFile = downloadCsvLocal(filePath)
    else:
        localFile = filePath

    if path.exists(localFile):
        with open(localFile) as csvFile:
            csvReader = csv.DictReader(csvFile)
            for i, rows in enumerate(csvReader):
                jsonfile.append(json.dumps(rows, indent=4, sort_keys=True))
                pprint.pprint(json.loads(jsonfile[i]), depth=4, width=80)
                print("")
    else:
        print(f"File: {filePath} could not be found")

if __name__ == '__main__':
    if len(sys.argv[1:]) < 1:
        print("No CSV files given at Command Line")
        print("Using default CSV sample from: https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv")
        print("*"*80)
        csvToJson("https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv")
        print("-" * 80)
        print(f"End of default CSV Sample")
    else:
        for file in sys.argv[1:]:
            print("*" * 80)
            print(f"Converting {file} to JSON")
            print("*" * 80)
            csvToJson(file)
            print("-" * 80)
            print(f"End of: {file}\n")
