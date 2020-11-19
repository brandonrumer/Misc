#!/usr/local/bin/python3

'''
Checks the inventory of the Microsoft Xbox X console on BHPhoto and NewEgg.

Best Buy, Target, and Walmart actually have APIs but you need to be registered
 with them to get an API key. 'Free' email accounts won't work. I'll work on that...

This works on Linux under Python3. You need: 'sudo apt install sox' on a 
 Debian-based system.
''''


import requests, time, os
from bs4 import BeautifulSoup

def beep():
    duration = 20  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


def main():
    check()


def newegg():
    print('Checking NewEgg')
    try:
        producturl = 'https://www.newegg.com/p/N82E16868105273'
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        stock = soup.find('div', {'class':'product-inventory'})
        if 'OUT OF STOCK' not in stock.text.strip():
            print('Newegg: ' , stock.text.strip())
            beep()
        elif 'OUT OF STOCK' in stock.text.strip():
            print('Newegg: ' , stock.text.strip())
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


def bhphoto():
    print('Checking BHPhotoVideo')
    try:
        #producturl = 'https://www.bhphotovideo.com/c/product/1573218-REG/microsoft_234_00001_xbox_one_s_1tb.html'
        producturl = 'https://www.bhphotovideo.com/c/product/1600080-REG/microsoft_rrt_00001_xbox_series_x_1tb.html'
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            stock = soup.find('span', {'data-selenium':'stockStatus'})
            if 'In Stock' in stock.text.strip():
                print('BHPhotoVideo: ' , stock.text.strip())
                beep()
            elif 'In Stock' not in stock.text.strip():
                print('BHPhotoVideo: Not in stock')
        except Exception:
            print('BHPhtoVideo: String Not found (Probably out of stock)')
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


def bestbuy():
    print('Checking Best Buy')
    apiurl = 'https://www.bestbuy.com/products/6428324.json'
    page = requests.get(apiurl)
    print(page)
    print(page.text)


def check():
    bhphoto()
    newegg()
    print('Sleeping for 60 seconds')
    print('\n')
    time.sleep(60)
    try:
        check()
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


if __name__ == "__main__":
    main()

