import os
import shutil
import sys

import requests

CACHE_DIR = 'cache/'
IMAGE_DIR_PATH = CACHE_DIR + 'img/'


def validate_cache_dirs_exist():
    os.makedirs(IMAGE_DIR_PATH, exist_ok=True)


def fetch_and_cache_photo(file_url):
    validate_cache_dirs_exist()

    split_url = file_url.split('/')
    file_name = split_url[len(split_url)-1]
    full_path = IMAGE_DIR_PATH + file_name

    if os.path.exists(full_path):
        return full_path
    else: # if image is not already cached, fetch and cache it
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'User-Agent': 'Mozilla / 5.0 (X11;Linux x86_64; rv: 109.0) Gecko/20100101 Firefox/115.0'}
        response = requests.get(file_url, headers=headers, stream=True)
        if response.status_code == 200:
            image = response.raw
            with open(full_path, 'wb') as out_file:
                shutil.copyfileobj(image, out_file)
                out_file.close()

                return full_path
        else:
            print('Failed to receive photo for ' + file_url)
            return '-'

