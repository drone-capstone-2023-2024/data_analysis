import os
import sys

import requests
from bs4 import BeautifulSoup

from cache_util import fetch_and_cache_photo


class DroneDatasetExtractor:
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'User-Agent': 'Mozilla / 5.0 (X11;Linux x86_64; rv: 109.0) Gecko/20100101 Firefox/115.0'}

    url = 'https://drones.cnas.org/drones/'
    local_copy_path = 'drone-repo-page.html'  # Note to self: this code was written for the site version as of Aug 30, 2023

    site_contents = ''

    def __init__(self):
        if os.path.exists(self.local_copy_path):
            f = open(self.local_copy_path, "r")
            self.site_contents = f.read()
            print('loaded local copy of site')
        else:
            response = requests.get(self.url, headers=self.headers)

            if response.status_code == 200:
                print('pulled new local copy of site')
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

        drone_entry_elements = soup.find_all(class_='drone-box')

        drones = []  # List of drones
        for element in drone_entry_elements:
            details = {}  # details to add to drone list

            drone_details_element = element.find(class_='drone-details')

            # Get photo
            photo_element = element.find(class_='drone-name has-thumbnail')
            if photo_element is not None:
                photo_url = photo_element.attrs['style'].lstrip('background-image:url(\'').rstrip('\');')
                details['picture'] = fetch_and_cache_photo(photo_url)
            else:
                details['picture'] = '-'  # Picture not found

            # Get all remaining text details
            info_titles = drone_details_element.find('dl').find_all('dt')
            info_details = drone_details_element.find('dl').find_all('dd')

            index = 0
            for info_title in info_titles:
                details[info_title.next] = info_details[index].next

                index += 1

            drones.append(details)

        return drones


if __name__ == "__main__":
    datasetExtractor = DroneDatasetExtractor()

    print(datasetExtractor.extract_details())