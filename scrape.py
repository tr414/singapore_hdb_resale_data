from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
import json

URL = "https://en.wikipedia.org/wiki/List_of_Singapore_MRT_stations"
base = "https://en.wikipedia.org"
path = "your-file-path"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"}
page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser")

all_links = soup1.find_all("a")
count = 0
to_visit = []
for link in all_links:
    try:
         wiki_link = link['href']
    except:
        continue
    
    if wiki_link[1:5] == 'wiki' and wiki_link[-11:-1] == 'MRT_statio':
        to_visit.append(wiki_link)
        
stations = {}
for link in to_visit:
    URL = base + link
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    try:
        station = soup1.find("span", {"class": "mw-page-title-main"}).text[0:-12]
    except:
        station = link
    try: 
        date = soup1.find("span", {"class": "bday dtstart published updated"}).text
    except:
        date = None
        print(station)
    latitude = None
    longitude = None
    page_links = soup1.find_all("a")
    for p_link in page_links:
        try:
            if p_link['href'][0:9] == '//geohack':
                #print(p_link['href'][2:])
                coord = 'https://' + p_link['href'][2:]
                geo_coord = requests.get(coord, headers=headers)
                soup2 = BeautifulSoup(geo_coord.content, "html.parser")
                try:
                    latitude = float(soup2.find("span", {"class": "latitude p-latitude"}).text)
                    longitude = float(soup2.find("span", {"class": "longitude p-longitude"}).text)
                except:
                    print(station + "No coordinates found")
                break
        except:
            continue
    
    stations[station] = (date, latitude, longitude)

json_obj = json.dumps(stations, indent = 3)

with open(path + "mrt.json", "w") as f:
    f.write(json_obj)

print(stations)


"""
for row in rows:
        #print(row)
        h = row.find('th')
        if h:
            h = h.text
        else:
            continue
        if h == "Opened":
            d = row.find('td')
            if d:
                d_act = d
                d = d.text
                print(h)
                print(d_act)
                print(d)
            else:
                continue
            
        else:
            continue
        break

#latitude = soup1.find("span", {"class": "latitude"})
    #longitude = soup1.find("span", {"class": "longitude"})
    #print(latitude.text, longitude.text)
"""
