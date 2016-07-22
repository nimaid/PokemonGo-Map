import webbrowser
from getpass import getpass
from subprocess import *
from time import sleep
import requests
import json
import os

chromePath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
firefoxPath = 'C:/Program Files/Mozilla Firefox/Firefox.exe'
port = 5000
ngrokTitle = 'Use the http://xxxxxxxx.ngrok.io address!'
serverScript = 'example.py'
locale = 'en'
refreshTime = 5

full_path = os.path.realpath(__file__)
(path, filename) = os.path.split(full_path)

pokemonsFile = open(path + '/locales/pokemon.' + locale + '.json')
pokemonsJSON = json.load(pokemonsFile)
pokemonsFile.close()

loginFile = open(path + '/user/login.json', 'r+')
loginJSON = json.load(loginFile)
loginFile.seek(0)

settingsFile = open(path + '/user/settings.json', 'r+')
settingsJSON = json.load(settingsFile)
settingsFile.seek(0)

#get location
print('Below you will provide your location. This can be an address, coordinates, or anything you would type into google maps.')
print('You can also type "auto" (no quotes) to use your IP location, although this has terrible accuracy.')
location = raw_input('\nEnter your location: ')
if location == 'auto':
    print('Getting IP location...')
    r = requests.get('http://freegeoip.net/json')
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']

    location = '{} {}'.format(lat, lon)

    print('Your IP location is {}'.format(location))

#ask if use saved login
useSavedLogin = 'N'
if not loginJSON['new']:
    useSavedLogin = raw_input('\nDo you want to use "{}" (Y/N): '.format(loginJSON['username'])).upper()
    while (useSavedLogin != 'Y') and (useSavedLogin != 'N'):
        useSavedLogin = raw_input('Invalid choice. Use "{}" (Y/N): '.format(loginJSON['username'])).upper()

login = {'new': False}
password = ''

if useSavedLogin == 'Y':
    login = loginJSON
elif useSavedLogin == 'N':
    #get login type and details
    login['type'] = raw_input('\nDo you want to log in with Google (google) or Pokemon Trainer Club (ptc): ').lower()
    while (login['type'] != 'google') and (login['type'] != 'ptc'):
        login['type'] = raw_input('\nInvalid login type. Please choose either google or ptc: ').lower()

    if(login['type'] == 'google'):
        login['username'] = raw_input('\nEnter your Google username (Example: foobar@gmail.com, or just foobar): ')
        if login['username'].find('@') == -1:
            login['username'] += '@gmail.com'
    elif(login['type'] == 'ptc'):
        login['username'] = raw_input('\nEnter your Pokemon Trainer Club username: ')

    #ask if save login
    saveLogin = raw_input('\nDo you want to save this login for next time (Y/N): ').upper()
    while (saveLogin != 'Y') and (saveLogin != 'N'):
        saveLogin = raw_input('Invalid choice. Save login (Y/N): ').upper()

    if saveLogin == 'Y':
        loginFile.write(json.dumps(login))

loginFile.close()

if login['type'] == 'google':
    password = getpass('\nEnter your password for your Google account "{}" (will be invisible): '.format(login['username']))
elif login['type'] == 'ptc':
    password = getpass('\nEnter your password for your Pokemon Trainer Club account "{}" (will be invisible): '.format(login['username']))

#test if there are saved settings
useSaved = 'N'
if not settingsJSON['new']:
    #ask if use saved settings
    useSaved = raw_input('\nDo you want to use saved settings (Y/N): ').upper()
    while (useSaved != 'Y') and (useSaved != 'N'):
        useSaved = raw_input('Invalid choice. Use saved settings (Y/N): ').upper()

settings = {'new':False}
if useSaved == 'N':
    #ask for search radius
    print('\nBelow you will enter the search radius limit, in steps.')
    print('Each step is equal to 50 meters.')
    print('A higher number here will mean the maps takes longer to populate and refresh.')
    print('A good starting point to try is 10 steps.')
    steps = raw_input('\nEnter search radius limit: ')
    while not steps.isdigit():
        steps = raw_input('Invalid number. Enter search radius limit: ')

    steps = int(steps)
    if steps == 0:
        steps = 1

    settings['st'] = steps

    #ask if display gyms
    dgRaw = raw_input('\nDo you want to display gyms (Y/N): ').upper()
    while (dgRaw != 'Y') and (dgRaw != 'N'):
        dgRaw = raw_input('Invalid choice. Display gyms (Y/N): ').upper()

    if dgRaw == 'Y':
        settings['dg'] = True
    elif dgRaw == 'N':
        settings['dg'] = False

    #ask if display pokestops
    dpRaw = raw_input('\nDo you want to display pokestops (Y/N): ').upper()
    while (dpRaw != 'Y') and (dpRaw != 'N'):
        dpRaw = raw_input('Invalid choice. Display pokestops (Y/N): ').upper()

    if dpRaw == 'Y':
        settings['dp'] = True
        #ask if display only lured pokestops
        olRaw = raw_input('\nDo you want to display only pokestops with active lure modules (Y/N): ').upper()
        while (olRaw != 'Y') and (olRaw != 'N'):
            olRaw = raw_input('Invalid choice. Display only pokestops w/ lure (Y/N): ').upper()

        if olRaw == 'Y':
            settings['ol'] = True
        elif olRaw == 'N':
            settings['ol'] = False
    elif dpRaw == 'N':
        settings['dp'] = False

    #ask if whitelist, blacklist, or all
    print('\nBelow you will chose which pokemon to display.')
    print('The first option is to whitelist pokemon, AKA only display specific ones.')
    print('The second option is to blacklist pokemon, AKA display all but specific ones.')
    print('The third option is to display all pokemon.')
    filterRaw = raw_input('\nWhitelist (W), blacklist (B), or display all (A): ').upper()
    while (filterRaw != 'W') and (filterRaw != 'B') and (filterRaw != 'A'):
        filterRaw = raw_input('Invalid choice. Whitelist (W), blacklist (B), or display all (A): ').upper()

    settings['filter'] = filterRaw
    
    if filterRaw == 'W':
        print('\nBelow you will enter a comma seperated list of the pokemon you wish to show.')
        print('You may either use the pokemon ID or the pokemon name (with first letter capitalized')
        print('For example, you could enter either 133 or {}.'.format(pokemonsJSON['133']))
        print('Therefore, an example entry would be: ')
        print('\n133,{},135,{}'.format(pokemonsJSON['134'], pokemonsJSON['136']))
        print('\nIf you mispell a name, or fail to capitalize it\'s first letter, it will not be shown.')
        pokemon = raw_input('\nPokemon to show: ').replace(' ', '')
        settings['fpokemon'] = pokemon
    elif filterRaw == 'B':
        print('\nBelow you will enter a comma seperated list of the pokemon you wish to hide.')
        print('You may either use the pokemon ID or the pokemon name (with first letter capitalized')
        print('For example, you could enter either 16 or {}.'.format(pokemonsJSON['16']))
        print('Therefore, an example entry would be: ')
        print('\n13,{},41,{}'.format(pokemonsJSON['16'], pokemonsJSON['19']))
        print('\nIf you mispell a name, or fail to capitalize it\'s first letter, it will not be hidden.')
        pokemon = raw_input('\nPokemon to hide: ').replace(' ', '')
        settings['fpokemon'] = pokemon

    #ask if save settings
    saveRaw = raw_input('\nDo you want to save these settings for next time (Y/N): ').upper()
    while (saveRaw != 'Y') and (saveRaw != 'N'):
        saveRaw = raw_input('Invalid choice. Save settings (Y/N): ')

    if saveRaw == 'Y':
        settingsFile.write(json.dumps(settings))

elif useSaved == 'Y':
    settings = settingsJSON
    
#build command string
#initialize the command string
cmdStr = 'C:\Python27\python.exe {}'.format(serverScript)
cmdStr += ' -a {}'.format(login['type'])
cmdStr += ' -u {}'.format(login['username'])
cmdStr += ' -p {}'.format(password)

cmdStr += ' -l "{}"'.format(location)

cmdStr += ' -ar {}'.format(refreshTime)

cmdStr += ' -st {}'.format(settings['st'])
if settings['dg']:
    cmdStr += ' -dg'
if settings['dp']:
    cmdStr += ' -dp'
    if settings['ol']:
        cmdStr += ' -ol'
if settings['filter'] != 'A':
    if settings['filter'] == 'W':
        cmdStr += ' -o '
    elif settings['filter'] == 'B':
        cmdStr += ' -i '
    cmdStr += settings['fpokemon']

#close the settings file
settingsFile.close()

#ask if expose server to the internet
print('\nBelow you will choose whether to expose your server to the internet.')
print('If you do, it will create a URL from which you can view your server, anywhere in the world, on any device.')
print('If you don\'t, it will just run locally, and your browser will open to the map.')
exposeRaw = raw_input('\nDo you want to expose your server to the internet (Y/N): ').upper()
while (exposeRaw != 'Y') and (exposeRaw != 'N'):
    exposeRaw = raw_input('Invalid choice. Expose to internet (Y/N): ').upper()

#give warning
os.system('cls')
if exposeRaw == 'N':
    print('If no browser pops up after about 10 seconds, manually type "localhost:{}" into a browser.'.format(port))
    print('Note that this will only be visible on your computer.')
    print('Close this window when you\'re done.')
elif exposeRaw == 'Y':
    print('After about 10 seconds, a second window will pop up. Let both run.')
    print('Find the URL in this new window in the form of http://xxxxxxxx.ngrok.io')
    print('You can type this URL into any browser, even your phone\'s!')
    print('Close both windows when you\'re done.')
print('\nAlso, if no pokemon show up after a while, make sure the servers aren\'t down...')
raw_input('\nPress enter to start the search!...')
os.system('cls')

#start the script
Popen(cmdStr)

#wait
sleep(10)

if exposeRaw == 'Y':
    #start ngrok
    ngrok = 'start "{}" "{}/ngrok.exe" http {}'.format(ngrokTitle, path, port)
    os.system(ngrok)
elif exposeRaw == 'N':
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

    url = 'http:\\localhost:{}'.format(port)

    if chrome != False:
        chrome.open(url)
    elif firefox != False:
        firefox.open(url)
    else:
        webpage.open(url)
