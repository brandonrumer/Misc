import requests
import time
from datetime import datetime
import winsound
import platform
import getpass
import traceback
import smtplib
import ssl
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def checkstock(operatingsystem, password):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time: ", current_time)

    url = "https://www.basspro.com/shop/en/131624"

    payload = {}
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except:
        print('Pausing due to requests error')
        time.sleep(60)

    # What to key off of. In this case, the page doesn't exist if there's no inventory
    nostock = 'This product has either been removed or is no longer available for sale.'

    try:
        if nostock in response.text:
            print('Nothing in stock')
        elif nostock not in response.text:
            print('you might have bullets')
            sendmail(password)
            beep(operatingsystem)
            print('')
            sys.exit(0) # remove if it should loop

    except Exception:
        print('Ran into an exception in parsing the data')
        print(traceback.print_exc())
    except KeyboardInterrupt:
        print('Quitting...')
        quit()

    print('Sleeping for 120 seconds.')
    print('' * 3)


def sendmail(password):
    sender_email = "someguyspythonmailer@gmail.com"    # Enter your address
    receiver_email = "brumer0@gmail.com"    # Enter receiver address

    message = MIMEMultipart("alternative")
    message["Subject"] = "BassPro 30-06 Ammo in Stock!"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Hi,

    There should be ammo in stock:
    https://www.basspro.com/shop/en/131624

    """
    part1 = MIMEText(text, "plain")
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
          sender_email, receiver_email, message.as_string()
        )


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
            operatingsystem = 'Linux'
        return operatingsystem
    except Exception:
        print('error in getting OS information.')
        quit()
    except KeyboardInterrupt:
        quit()


def beep(operatingsystem):
    if operatingsystem == 'Linux':
        duration = 20    # seconds
        freq = 440    # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    if operatingsystem == 'Windows':
        print('beeping windows!')
        for i in range(1, 50):
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)


def main():
    password = getpass.getpass(prompt='GMail sender password: ')
    operatingsystem = getplatform()
    while True:
        try:
            checkstock(operatingsystem, password)
            time.sleep(120)
        except Exception:
            print('Ran into an exception in check function. Pausing for 60 seconds.')
            print(traceback.print_exc())
            time.sleep(60)
        except KeyboardInterrupt:
            print('Quitting...')
            quit()


if __name__ == "__main__":
    main()
