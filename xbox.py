#!/usr/local/bin/python3

'''
Checks the inventory of the Microsoft Xbox X console on BHPhoto and NewEgg.

Best Buy, Target, and Walmart actually have APIs but you need to be registered
 with them to get an API key. 'Free' email accounts won't work. I'll work on that...

 UPDATE: I found that popfindr.com can pull inventory, and then I can statically
 scrape inventory from the results. This is for the Target and Best Buy inventory
 in Fayetteville NC. Use Firefox Developer to pull the right page from PopFindr.

This works on Linux under Python3. You need: 'sudo apt install sox' on a 
 Debian-based system.
'''


import requests, time, os
from bs4 import BeautifulSoup

import pandas as pd

def beep():
    duration = 20  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


def main():
    print('\n')
    try:
        check()
    except Exception:
        print('Ran into exception in Main!!')
    except KeyboardInterrupt:
        print(Quitting)
        quit()


    
def newegg():
    #print('Checking NewEgg')
    try:
        producturl = 'https://www.newegg.com/p/N82E16868105273'
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        stock = soup.find('div', {'class':'product-inventory'})
        if 'OUT OF STOCK' not in stock.text.strip():
            print('-----------Newegg-----: ' , stock.text.strip())
            beep()
        elif 'OUT OF STOCK' in stock.text.strip():
            print('Newegg: ' , stock.text.strip())
    except KeyboardInterrupt:
        print('Quitting...')
        quit()
    except Exception:
        print('Ran into an exception in NewEgg. Likely a request error.')


def bhphoto():
    #print('Checking BHPhotoVideo')
    try:
        #producturl = 'https://www.bhphotovideo.com/c/product/1573218-REG/microsoft_234_00001_xbox_one_s_1tb.html'
        producturl = 'https://www.bhphotovideo.com/c/product/1600080-REG/microsoft_rrt_00001_xbox_series_x_1tb.html'
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            stock = soup.find('span', {'data-selenium':'stockStatus'})
            if 'In Stock' in stock.text.strip():
                print('-----------------BHPhotoVideo: -------' , stock.text.strip())
                beep()
            elif 'In Stock' not in stock.text.strip():
                print('BHPhotoVideo: Not in stock.')
        except Exception:
            print('BHPhtoVideo: String Not found (Probably out of stock).')
    except KeyboardInterrupt:
        print('Quitting...')
        quit()
    except Exception:
        print('Ran into an exception in bhphoto. Likely a request error.')        


def adorama():
    try:
        producturl = 'https://www.adorama.com/xbrrt00001b.html'
        page = requests.get(producturl)
        print(page.text)
        quit()
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            #stock = soup.find('button', {'data-orig-value':'Temporarily not available'})
            stock = soup.find('button', {'class':'button trackEvent add-to-cart action inverse'})
            '''
            if 'In Stock' in stock.text.strip():
                print('BHPhotoVideo: ' , stock.text.strip())
                beep()
            elif 'In Stock' not in stock.text.strip():
                print('BHPhotoVideo: Not in stock')
            '''
            print(stock.text)
        except Exception:
            print('Adorama: String Not found (Probably out of stock)')
    except KeyboardInterrupt:
        print('Quitting...')
        quit()
    except Exception:
        print('Ran into an exception in Adorama. Likely a request error.')



def PopFindrTarget():
    producturl = 'https://popfindr.com/results?pid=207-41-0001&zip=28348&range=25&webpage=target&token=03AGdBq25xvIZKDLjisiS4_S--HVo_I0H9oBXwwy_RPqFAu4dosj6ThW_rh1aGOZIjWZKY2hM0aM-MzL7Z40PrumdmaPUnkSBTG5i5tNezWCsjxQ4BX4VghDWdB1OFJSJS2WlmH0S-HTIfNnZWwbJ2rLG1sWsSf6oAtBr9oM73i_oWI3SVCQnRCXjA5bK3nMppvtWmAp6UXA40QslzFr-dqc6oadbohkkHjezScChv1cjDP70RzWOYDsr4Qi5SVKezFc0ZnkayUOd1cGW65_OeVT19DZd7S1ShubhVIsLRry0ZYQ5xdbqIPkHas3ren5O34UIWFDMMCR15m_YtcufuXbaL8JxcdBPHUWaFgtl7K7UDqyuVGBw-QRt14lJXAeBudgw0-yVJTGmpkYPcCe_493ePWBN0TbsC3sNua6dGlVNUymESm7BteffBV3ztTyX8ihjhCwwO6F3oBCbu05pWFQie513TA6o-qlI5hwydRQHkWgJ-WkeV6kA'
    try:
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            tables = soup.find_all('table')[1]
            row = tables.find_all('tr')[1]
            cell = row.find_all('th')[2]
            inventory = cell.text.strip()
            if inventory is '0':
                print(f'Target has {inventory} IN STOCK!')
                beep()
            elif inventory is not '0':
                print(f'Target has {inventory}.')
        except Exception:
            print('Target: String Not found (Probably out of stock)')
    except Exception:
        print('Ran into an exception in PopFindr Target. Likely a request error.')
    except KeyboardInterrupt:
        print('Quitting...')
        quit()



def PopFindrBestBuy():
    producturl = 'https://popfindr.com/results?pid=6428324&zip=28348&range=25&webpage=bestbuy&token=03AGdBq27W1_OQsSNJW8bf-JBDrP8rU5xOwMy_Mi65vTZvU0RrYe-FBmslESjnNN2fh6ODHOVcxkl3jFMTdP8BV9-z0n2rp_5gxWPt32-IpmEhBK73oixHOvvsUKZM08S40xCLuPMt6oRYN8-X3zkOMBi1muqAs7Oy1IgDkYzX53zl12uXbEF712T-qMy0yCDJDKpOALYCHDWmXrrrkY8sQGUvZbsg0JfPHBo4bno3j9D0hx0iJ3z-BAJKkbvmmOve0yKuk-H91xP4G2ESTANHHVQKcrijxciAw3QNn8Px-yfBY6t232-FcpEsVv_5-KC9d96TE52o652tldztV-YQlRbVFTChJHkPH-ErF2x1ehKNis6PAcbhG4ywhcX9LgEp6eyqfNyh0oYwurPAdtojd5XFo_yoRvCSx7iun1AALIkrDSC4rLZMfiXU5OMuMYHwSHD_3BSsYQ4M7xBMy1AlwaqtbQ2Czvf_tQ'
    try:
        page = requests.get(producturl)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            tables = soup.find_all('table')[1]
            row = tables.find_all('tr')[1]
            cell = row.find_all('th')[2]
            inventory = cell.text.strip()
            if inventory is '0':
                print(f'Best Buy has {inventory} IN STOCK!')
                beep()
            elif inventory is not '0':
                print(f'Best Buy has {inventory}.')
        except Exception:
            print('Target: String Not found (Probably out of stock)')
    except Exception:
        print('Ran into an exception in PopFindr Best Buy. Likely a request error.')
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


def check():
    PopFindrBestBuy()
    PopFindrTarget()
    bhphoto()
    newegg()
    print('\n')
    print('Sleeping for 60 seconds')
    time.sleep(45)
    try:
        check()
    except Exception:
        print('Ran into an exception in check function. Pausing for 60 seconds.')
        time.sleep(60)
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


if __name__ == "__main__":
    main()

