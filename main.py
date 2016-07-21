import webbrowser
from getpass import getpass
from os import system
import subprocess
from time import sleep
import requests
import json
import os

chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
firefoxPath = 'C:/Program Files/Mozilla Firefox/Firefox.exe'
url = 'http://localhost:5000'
serverScript = 'example.py'
locale = 'en'

full_path = os.path.realpath(__file__)
(path, filename) = os.path.split(full_path)
pokemonsJSON = json.load(open(path + '/locales/pokemon.' + locale + '.json'))

#get location
print('Below you will provide your location. This can be an address, coordinates, or anything you would type into google maps.')
print('You can also type "auto" (no quotes) to use your IP location, although this has poor accuracy.')
location = raw_input('\nEnter your location: ')
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

loginType = raw_input('\nDo you want to log in with Google (google) or Pokemon Trainer Club (ptc): ').lower()
while (loginType != 'google') and (loginType != 'ptc'):
    loginType = raw_input('\nInvalid login type. Please choose either google or ptc: ').lower()

if(loginType == 'google'):
    username = raw_input('\nEnter your Google username (Example: foobar@gmail.com): ')

    password = getpass('Enter your Google password: ')
elif(loginType == 'ptc'):
    username = raw_input('\nEnter your Pokemon Trainer Club username: ')

    password = getpass('Enter your Pokemon Trainer Club password: ')

#initialize the command string
cmdStr = 'C:\Python27\python.exe {} -a {} -u {} -p {} -l "{}" -st 10 -ar 5'.format(serverScript, loginType, username, password, location)

#ask if display gyms
dgRaw = raw_input('\nDo you want to display gyms (Y/N): ').upper()
while (dgRaw != 'Y') and (dgRaw != 'N'):
    dgRaw = raw_input('Invalid choice. Display gyms (Y/N): ').upper()

if dgRaw == 'Y':
    cmdStr += ' -dg'

#ask if display pokestops
dpRaw = raw_input('\nDo you want to display pokestops (Y/N): ').upper()
while (dpRaw != 'Y') and (dpRaw != 'N'):
    dpRaw = raw_input('Invalid choice. Display pokestops (Y/N): ').upper()

if dpRaw == 'Y':
    cmdStr += ' -dp'
    
    #ask if display only lured pokestops
    olRaw = raw_input('\nDo you want to display only pokestops with active lure modules (Y/N): ').upper()
    while (olRaw != 'Y') and (olRaw != 'N'):
        olRaw = raw_input('Invalid choice. Display only pokestops w/ lure (Y/N): ').upper()

    if olRaw == 'Y':
        cmdStr += ' -ol'

#ask if whitelist, blacklist, or all
print('\nBelow you will chose which pokemon to display.')
print('The first option is to whitelist pokemon, AKA only display specific ones.')
print('The second option is to blacklist pokemon, AKA display all but specific ones.')
print('The third option is to display all pokemon.')
filterRaw = raw_input('\nWhitelist (W), blacklist (B), or display all (A): ').upper()
while (filterRaw != 'W') and (filterRaw != 'B') and (filterRaw != 'A'):
    filterRaw = raw_input('Invalid choice. Whitelist (W), blacklist (B), or display all (A): ').upper()

if filterRaw == 'W':
    cmdStr += ' -o '
    print('\nBelow you will enter a comma seperated list of the pokemon you wish to show.')
    print('You may either use the pokemon ID or the pokemon name (with first letter capitalized')
    print('For example, you could enter either 133 or {}.'.format(pokemonsJSON['133']))
    print('Therefore, an example entry would be: ')
    print('\n133,{},135,{}'.format(pokemonsJSON['134'], pokemonsJSON['136']))
    #print('\n!!!DO NOT INCLUDE SPACES!!!')
    print('\nIf you mispell a name, or fail to capitalize it\'s first letter, it will not be shown.')
    pokemon = raw_input('\nPokemon to show: ').replace(' ', '')
    cmdStr += pokemon
elif filterRaw == 'B':
    cmdStr += ' -i '
    print('\nBelow you will enter a comma seperated list of the pokemon you wish to hide.')
    print('You may either use the pokemon ID or the pokemon name (with first letter capitalized')
    print('For example, you could enter either 16 or {}.'.format(pokemonsJSON['16']))
    print('Therefore, an example entry would be: ')
    print('\n13,{},41,{}'.format(pokemonsJSON['16'], pokemonsJSON['19']))
    #print('\n!!!DO NOT INCLUDE SPACES!!!')
    print('\nIf you mispell a name, or fail to capitalize it\'s first letter, it will not be hidden.')
    pokemon = raw_input('\nPokemon to hide: ').replace(' ', '')
    cmdStr += pokemon

#start the script
subprocess.Popen(cmdStr)

#wait
sleep(10)

#launch the webpage
chrome = False
firefox = False

try:
    chrome = webbrowser.get(chromePath)
except:
    print('INFO: Chrome not found. (It\'s okay to ignore this.)')
    
try:
    firefox = webbrowser.get(firefoxPath)
except:
    print('INFO: Firefox not found. (It\'s okay to ignore this.)')

if chrome != False:
    chrome.open(url)
elif firefox != False:
    firefox.open(url)
else:
    webpage.open(url)
