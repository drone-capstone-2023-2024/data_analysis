import os
import sys

import requests
from bs4 import BeautifulSoup


class DroneDatasetExtractor:
    url = 'https://drones.cnas.org/drones/'
    local_copy_path = 'drone-repo-page.html'  # Note to self: this code was written for the site version as of Aug 30, 2023

    site_contents = ''

    def init(self):
        if os.path.exists(self.local_copy_path):
            f = open(self.local_copy_path, "r")
            self.site_contents = f.read()
        else:
            headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'User-Agent': 'Mozilla / 5.0 (X11;Linux x86_64; rv: 109.0) Gecko/20100101 Firefox/115.0'
                       }
            response = requests.get(self.url, headers=headers)

            if response.status_code == 200:
                self.site_contents = response.text
            else:
                print('Failed to retrieve the web page. Status code:', response.status_code)
                sys.exit(1)

            # Dump website to file for local cache
            f = open(self.local_copy_path, "w")
            f.write(response.text)
            f.close()

    def extract_details(self):
        soup = BeautifulSoup(self.site_contents, 'html.parser')

        drone_details_elements = soup.find_all(class_='drone-details')

        drones = []  # List of drones
        for element in drone_details_elements:
            info_titles = element.find('dl').find_all('dt')
            info_details = element.find('dl').find_all('dd')

            details = {}  # details to add to drone list
            index = 0
            for info_title in info_titles:
                details[info_title.next] = info_details[index].next

                index += 1

            drones.append(details)

        print(drones)

        return drones
