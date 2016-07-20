import webbrowser
from getpass import getpass
from os import system
import subprocess
from time import sleep
import requests
import json

chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
firefoxPath = 'C:/Program Files/Mozilla Firefox/Firefox.exe'
url = 'http://localhost:5000'

#get location
location = raw_input('Enter your location, or type "auto" (no quotes) to ise IP location: ')
if location == 'auto':
    print('Getting IP location...')
    r = requests.get('http://freegeoip.net/json')
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    location = '{} {}'.format(lat, lon)

    print('Your IP location is {}'.format(location))

#get login type and details
username = ''
password = ''

loginType = raw_input('Do you want to log in with Google (google) or Pokemon Trainer Club (ptc): ').lower()
while (loginType != 'google') and (loginType != 'ptc'):
    loginType = raw_input('Invalid login type. Please choose either google or ptc: ').lower()

if(loginType == 'google'):
    username = raw_input('Enter your Google username (ommit the @gmail.com): ')
    username += '@gmail.com'

    password = getpass('Enter your Google password: ')
elif(loginType == 'ptc'):
    username = raw_input('Enter your Pokemon Trainer Club username: ')

    password = getpass('Enter your Pokemon Trainer Club password: ')

#start the script
subprocess.Popen('C:\Python27\python.exe example.py -a {} -u {} -p {} -l "{}" -st 10 -ar 5 -dp -dg'.format(loginType, username, password, location))

#wait
sleep(10)

#launch the webpage
chrome = False
firefox = False

try:
    chrome = webbrowser.get(chromePath)
except:
    print('Chrome not found.')
    
try:
    firefox = webbrowser.get(firefoxPath)
except:
    print('Firefox not found.')

if chrome != False:
    chrome.open(url)
elif firefox != False:
    firefox.open(url)
else:
    webpage.open(url)
