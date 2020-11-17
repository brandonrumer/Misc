#!/usr/local/bin/python3

""" Summary:  
        A sample application showing how beautifulsoup can be leveraged in real-world 
        applications. This specific script searches Indeed for a job.


Usage:
        indeed.py [-h] [-j job] [-s state]

            Searches Indeed for a job in a state.

        optional arguments:
        -h, --help            show this help message and exit
        -j job, --job job     What job to look for. If using a space "double quotes" must be used.
        -s state, --state state
                                Where to look (MUST USE A 2 LETTER STATE CODE)


Requirements: 
    beautifulsoup
"""

import requests
import argparse
import math
from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser(description='Searches Indeed for a job in a state.', \
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-j',
        '--job', 
        action='store', 
        metavar='job', 
        required=False, 
        help='What job to look for. If using a space "double quotes" must be used.'
        )
    parser.add_argument(
        '-s',
        '--state', 
        action='store', 
        metavar='state', 
        required=False, 
        help='Where to look (MUST USE A 2 LETTER STATE CODE)'
        )
    args = parser.parse_args()

    # Fix any spaces in the job search
    args.job = args.job.replace(' ','+')


    url = f'https://www.indeed.com/jobs?q={args.job}&l={args.state}&start='

    # First we have to get the total number of jobs, and coorelate them to the number of 
    #   pages to search through. 
    page = requests.get(url+str('0'))
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find('div', attrs={'id': 'searchCountPages'})
    pages = result.text.strip()
    splitsentence = pages.split()
    totaljobs = splitsentence[3]
    #print(totalpages)

    # We have the total jobs, get the total pages to search through, in sections of 10
    pages = int(math.ceil(int(totaljobs) / 10.0))

    # Go through all the search results, 10 at a time and pull out the data
    for i in range(0, pages, 10):
        posturl = 'url' + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
        for x in results:
            try: 
                company = x.find('span', attrs={"class":"company"})
                print('Company:', company.text.strip())
                job = x.find('a', attrs={'data-tn-element': "jobTitle"})
                print('Job:', job.text.strip())
                location = x.find('span', attrs={"class":"location accessible-contrast-color-location"})
                print('Location:' , location.text.strip())
                print('\n')
            except AttributeError:
                pass


if __name__ == "__main__":
    main()
