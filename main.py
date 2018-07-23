import requests
from bs4 import BeautifulSoup
import hashlib
import json



def GenerateSID(key):

    page = requests.get("http://fritz.box/login_sid.lua")
    soup = BeautifulSoup(page.text, 'html.parser')

    challenge_value = soup.find('challenge').text
    password = challenge_value + '-' + key

    md5_value = hashlib.md5(password.encode('utf-16le')).hexdigest()
    page = requests.get("http://fritz.box/login_sid.lua?user=&response=" + challenge_value + "-" + md5_value)
    soup = BeautifulSoup(page.text, 'html.parser')
    sidvalue = soup.find('sid').text

    return sidvalue

def GenerateLua(sidvalue):

    wlan_page = requests.get("http://fritz.box/?sid=" + sidvalue + "&lp=netDev")
    wlan_soup = BeautifulSoup(wlan_page.text, 'html.parser')

    return ".lua?sid="+sidvalue

def WlanConnections(lua):

    list = []

    wifiSettingsURL = "http://fritz.box/wlan/wlan_settings" + lua
    wifiPage = requests.get(wifiSettingsURL)
    soup = BeautifulSoup(wifiPage.text, 'html.parser')

    row = soup.findAll('td', {'class': 'cut_overflow name'})

    for item in row:
        #checker = item.find('td', {'class':'wlan_rssi0'})
        #if(checker is None):
            print(item.prettify())

    #allNames = soup.findAll('td', {'class':'cut_overflow name'})
    #wlanRssi = soup.findAll('td,')


    #for name in allNames:
    #    if(name[''])
    #        print(name['title'])

    #print(soup.find('div', {'id':'uiKnownDevices'}).prettify())
    #print(soup.find('tbody', {'id': 'uiViewRow'}).prettify())

def main():
    
    sidvalue = GenerateSID()
    lua = GenerateLua(sidvalue)
    WlanConnections(lua)


    return 0

if __name__ == "__main__":
    main()

