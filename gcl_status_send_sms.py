import random
import requests
import sys
import time
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
from urllib.robotparser import RobotFileParser

file = open('twilio_auth.txt', 'r')
account_sid = ''
auth_token = ''
twilio_number = ''
my_number = ''
url = ''

if file.readline() == 'account_sid\n':
    account_sid = file.readline()[:-1]
if file.readline() == 'auth_token\n':
    auth_token = file.readline()[:-1]
if file.readline() == 'twilio_number\n':
    twilio_number = file.readline()[:-1]
if file.readline() == 'my_number\n':
    my_number = file.readline()[:-1]
if file.readline() == 'url\n':
    url = file.readline()[:-1]
    
file.close()

crawl_delay = 20
rp = RobotFileParser()
rp.set_url(url+'robots.txt')
rp.read()
if rp.crawl_delay(rp) != None:
    crawl_delay = rp.crawl_delay(rp)

# REMOVE
print(crawl_delay)
#sys.exit(0)

if account_sid == '' or auth_token == '' or twilio_number == '' or my_number == '':
    print('ERROR: Didn\'t find all relevant info')
    sys.exit(1)


client = Client(account_sid, auth_token)
now = datetime.now()

message = client.messages.create(
                        body='GCL SMS app started at ' + now.strftime("%m/%d/%Y, %H:%M:%S"),
                        from_=twilio_number,
                        to=my_number
                )
# REMOVE
#sys.exit(0)
print(type(message))

URL = url+'gc-loader-pnp.html'

message_body = 'GCLoader is up now.\n'+URL

print(message_body)
#sys.exit(0)
crawl_delay = 600
# CHANGE TO while true
time_offset = 0
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    try:
        page = requests.get(URL)
    except ConnectionError:
        print('Connection error')
        message = client.messages.create(
                              body='Connection error: connection reset',
                              from_=twilio_number,
                              to=my_number
                          )
        time.sleep(20)
        continue
    except KeyboardInterrupt:
        print('Ended')
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', {'title':'Availability'})
    # REMOVE not
    if ('Out of stock' in str(results)):
        print('Still out of stock at: ' + current_time)
    else:
        message = client.messages.create(
                              body=message_body,
                              from_=twilio_number,
                              to=my_number
                          )
        break
    time_offset = random.randrange(-50,50)
    time.sleep(crawl_delay+time_offset)

