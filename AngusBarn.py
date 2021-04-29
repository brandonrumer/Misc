#!/usr/local/bin/python3

""" Summary:  
        Checks for a reservation at the Angus Barn. 
    Usage:
        python AngusBarn.py
"""

import requests
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime
import winsound
import platform
import smtplib, ssl
import getpass


def sendmail(password):
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "@gmail.com"  # Enter your address
  receiver_email = "@gmail.com"  # Enter receiver address
  
  #password = getpass("Type your password and press enter: ")
  #password = ''
  


  message = f"""From: {sender_email}
  To: {receiver_email}
  SUBJECT:  An angus barn appointment is available\n
  This message is sent from Python.
  """

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, message)


def steak(operatingsystem, password):
  reservationdate = "05/22/2021"
  partysize = "5"
  reservationhour = "06" # I'm not messing w/the minute. 

  #payload = 'authenticity_token=DdzJj4j08MIGRXTa4Cqt/cvjgggCBJmj3MKOu/keU5g%3D&reservation%5Bdate%5D=05/22/2021&reservation%5Bparty_size%5D=5&reservation%5Btime%5D=06%3A00%20PM&reservation%5Bwidget_id%5D=72&utf8=%u2713'
  
  url = "http://widgets.espconnects.com/reservations/check.js"
  payload = f'authenticity_token=DdzJj4j08MIGRXTa4Cqt/cvjgggCBJmj3MKOu/keU5g%3D&reservation%5Bdate%5D={reservationdate}&reservation%5Bparty_size%5D={partysize}&reservation%5Btime%5D={reservationhour}%3A00%20PM&reservation%5Bwidget_id%5D=72&utf8=%u2713'
  headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
  }

  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  print("Current Time: ", current_time)

  try:
    response = requests.request("POST", url, headers=headers, data = payload)
    #print(response.text.encode('utf8'))
  except:
    print('Pausing due to requests error')
    time.sleep(60)

  # Parse the output for the times available
  try:
    soup = BeautifulSoup(response.content, 'html.parser')
    stock = soup.findAll('button', class_="button button3")
    print(f'These times are available on {reservationdate}:')
    for i in stock:
      print(i.text.strip())
      available = str(i.text.strip())
      if ('09' in available) or ('05' in available) or ('06' in available) or ('06' in available):
        print('BOOK NOW!!' *5)
        sendmail(password)
        beep(operatingsystem)
  except Exception:
    print('Ran into an exception in parsing the data')
  except KeyboardInterrupt:
    print('Quitting...')
    quit()

  print('Sleeping for 120 seconds.')
  print('' *3)

  
def getplatform():
    try:
        plt = platform.system()
        if plt == "Windows":
            print("Your system is Windows")
            operatingsystem = "Windows"
        elif plt == "Linux":
            print("Your system is Linux")
            operatingsystem = "Linux"
        elif plt == "Darwin":
            print("Your system is MacOS")
            operatingsystem = "Mac"
        else:
            #print("Unidentified system")
            operatingsystem='Linux'
        return operatingsystem
    except Exception:
        print('error in getting OS information.')
        quit()
    except  KeyboardInterrupt:
        quit()


def beep(operatingsystem):
    if operatingsystem == 'Linux':
        duration = 20  # seconds
        freq = 440  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    if operatingsystem =='Windows':
        print('beeping windows!')
        for i in range(1,50):
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)



def main():
  password = getpass.getpass(prompt='GMail sender password: ')
  operatingsystem = getplatform()
  while True:
    try:
      steak(operatingsystem, password)
      time.sleep(120)
    except Exception:
        print('Ran into an exception in check function. Pausing for 60 seconds.')
        time.sleep(60)
    except KeyboardInterrupt:
        print('Quitting...')
        quit()


if __name__ == "__main__":
  main()
