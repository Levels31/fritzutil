#! /usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import hashlib


def generate_sid(key):

    page = requests.get("http://fritz.box/login_sid.lua")
    soup = BeautifulSoup(page.text, 'html.parser')

    challenge_value = soup.find('challenge').text
    password = challenge_value + '-' + key

    md5_value = hashlib.md5(password.encode('utf-16le')).hexdigest()
    page = requests.get("http://fritz.box/login_sid.lua?user=&response=" 
        + challenge_value + "-" + md5_value)
    soup = BeautifulSoup(page.text, 'html.parser')
    sidvalue = soup.find('sid').text

    return sidvalue


def generate_lua(sidvalue):

    wlan_page = requests.get("http://fritz.box/?sid=" + sidvalue + "&lp=netDev")
    wlan_soup = BeautifulSoup(wlan_page.text, 'html.parser')

    return ".lua?sid="+sidvalue


def currently_active_devices(sid):
    """
    Receives a LUA_ID as input. Returns a list of all devices that are
    currently connected to the network
    """

    page = requests.request(method="GET", url="http://fritz.box/?sid=" + sid + "&lp=overview")

    soup = BeautifulSoup(page.text, 'html.parser')
    row = soup.findAll({'class': 'network list active no_column'})

    for item in row:
        print(item)


def wlan_connected(sid):
    """ 
        Receives a LUA-ID as input. Returns a list of all devices ever
        connected.

        Parameters
        ----------
        sid : String
            Session ID Number, needed for every request.
    """

    list = []

    wifiSettingsURL = "http://fritz.box/wlan/wlan_settings" + sid
    wifiPage = requests.get(wifiSettingsURL)
    soup = BeautifulSoup(wifiPage.text, 'html.parser')

    row = soup.findAll('td', {'class': 'cut_overflow name'})

    for item in row:
        list.add(item['title'])


def main():
    print("Please enter Passphrase for FritzBox Webinterface:")
    key = input()
    sid = generate_sid(key)
    lua = generate_lua(sid)
    wlan_connected(lua)
    # currently_active_devices(sid)

    return 0


if __name__ == "__main__":
    main()
