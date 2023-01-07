import requests
import time
import json
import os
from bs4 import BeautifulSoup
from pystyle import Write, Colors, Colorate, Center

banner = """


                                    ███▄ ▄███▓ ▄▄▄       ██▀███   ██▓ ███▄    █ ▓█████ 
                                   ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▓██▒ ██ ▀█   █ ▓█   ▀ 
                                   ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▒██▒▓██  ▀█ ██▒▒███   
                                   ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ░██░▓██▒  ▐▌██▒▒▓█  ▄ 
                                   ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒░██░▒██░   ▓██░░▒████▒
                                   ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░
                                   ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░ ▒ ░░ ░░   ░ ▒░ ░ ░  ░
                                   ░      ░     ░   ▒     ░░   ░  ▒ ░   ░   ░ ░    ░   
                                          ░         ░  ░   ░      ░           ░    ░  ░
                                                   
                                                  t.me/EmpereurMiro
                                                  
                                                  

"""

os.system("mode 130,40")
os.system("title Marine Tracking / t.me/EmpereurMiro")
os.system("cls")

print(Center.XCenter(Colorate.Vertical(Colors.blue_to_green, banner, 1)))

webhook_url = Write.Input("[?] Webhook Link >>> ", Colors.blue_to_green, interval=0.0025)
url = Write.Input("[?] ID of Marinetraffic >>> ", Colors.blue_to_green, interval=0.0025)
time.sleep(1.2)
os.system("cls")

position_received_added = False

while True:
  response = requests.get("https://marinetraffic.live/vessels/data.php/" + url + "/")

  soup = BeautifulSoup(response.text, "html.parser")

  values = []
  for th in soup.find_all("th"):
    if th.text in ["Longitude", "Latitude", "Position Received", "Area"]:
      if th.text == "Position Received":
        if not position_received_added:
          td = th.find_next_sibling("td")
          values.append({
            "name": th.text + " <a:notifications:1061256457762385950>",
            "value": td.text,
            "inline": True
          })
          position_received_added = True
      else:
        td = th.find_next_sibling("td")
        values.append({
          "name": th.text + " 🗺️",
          "value": td.text,
          "inline": True
        })

  for div in soup.find_all("div", class_="vpage-trip-slider d-flex flex-grow-1 w-100 transition-translatex"):
    h3s = div.find_all("h3")
    if len(h3s) >= 2:
      values.append({
        "name": "Départ 🛫",
        "value": h3s[0].text,
        "inline": True
      })
      values.append({
        "name": "Arrivée 🛬",
        "value": h3s[1].text,
        "inline": True
      })

    embed = {
      "title": "https://marinetraffic.live/vessels/data.php/" + url + "/",
      "fields": values
    }

    requests.post(webhook_url, json={"embeds": [embed]})

    print("Don't close this windows")
    time.sleep(3600)
    os.system("cls")
