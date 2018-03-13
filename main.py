import requests
from bs4 import BeautifulSoup
import hashlib
import json

page = requests.get("http://fritz.box/login_sid.lua")
soup = BeautifulSoup(page.text, 'html.parser')

challenge_value = soup.find('challenge').text
password = challenge_value + '-Gerike19'

md5_value = hashlib.md5(password.encode('utf-16le')).hexdigest()
page = requests.get("http://fritz.box/login_sid.lua?user=&response=" + challenge_value + "-" + md5_value)
soup = BeautifulSoup(page.text, 'html.parser')
sidvalue = soup.find('sid').text

wlan_page = requests.get("http://fritz.box/?sid=" + sidvalue + "&lp=netDev")
wlan_soup = BeautifulSoup(wlan_page.text, 'html.parser')
print(wlan_soup.prettify())
json_data=open(file_directory).read()

data = json.loads(json_data)
print(data)

# This is a commit test
# This is a commit test from my Mac

#print(soup)
#print(soup.prettify())
