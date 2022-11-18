#!/usr/bin/env python3

''' Summary: Finds old files & reports their total size
Decription:
    Analyzes a directory's files that are older than a certain
    date and reports the total size. Change the variables for the age, in days,
    and the file path. 
'''


''' Importing built-in modules '''
import os
from os.path import join, getsize, getmtime
from datetime import datetime


__author__ = "Brandon Rumer"
__version__ = "1.0.0"
__email__ = "brandon.rumer@gmail.com"
__status__ = "Production"


def fileage(filename, max_file_age):
    # Maximum file age to gather data on (in days)

    file_stat = os.stat(filename)
    last_modification = datetime.fromtimestamp(file_stat.st_mtime)    
    last_access = datetime.fromtimestamp(file_stat.st_atime)

    current_time = datetime.now()
    time_since_last_modification = current_time - last_modification
    time_since_last_access = current_time - last_access

    days_since_last_modification = time_since_last_modification.days
    days_since_last_access = time_since_last_access.days

    if days_since_last_access > max_file_age:
        file_size = getsize(filename)

        # comment out next 4 lines if you do not want to print progress
        msg = "{} was modified {} days ago, with last access {} days ago, and is {} bytes"
        msg = msg.format(filename, days_since_last_modification,
                        days_since_last_access, file_size)
        print(msg)

        return file_size


def main():
    ### HOW OLD OF FILES DO YOU WANT TO LOOK FOR , IN DAYS. No quotes ###
    max_file_age = 2
    ### FILE PATH YOU ARE SEARCHING , in quotes. If using a root path (c:\) use c:\\ ###
    path = 'C:\drop'

    total_size = 0
    file_count = 0
    total = []

    for root, dirs, files in os.walk(path):
        for name in files:
            a_file = join(root, name)
            file_size = fileage(a_file, max_file_age)
            # print(file_size)
            file_size = int(0 if file_size is None else file_size)

            total_size = int(total_size) + int(file_size)
            total.append(file_size)

    print('\n' * 3)
    print('Analyzed this directory: ' , path)
    # Add & print the size of all the items that met criteria
    numsum = sum(total)
    print("total size of items that meet date criteria: " , numsum)
    
    # Show the total amount of items that met criteria
    print("total items that meet date criteria: " , len(total))
    
    print('\n')


if __name__ == "__main__":
    main()
