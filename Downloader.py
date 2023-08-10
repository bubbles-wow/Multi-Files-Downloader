import os
import requests
from datetime import datetime
from email.utils import parsedate_to_datetime
import urllib.parse

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        last_modified_header = response.headers.get("Last-Modified")
        if last_modified_header:
            last_modified_datetime = parsedate_to_datetime(last_modified_header)
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            os.utime(save_path, (last_modified_datetime.timestamp(), last_modified_datetime.timestamp()))
            print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download: {url}")
        with open("errorurls.txt", "a") as f:
            f.write(url + "\n")
            f.close()


dir =  os.path.dirname(__file__)
base_save_dir = dir

if not os.path.exists(base_save_dir):
    os.makedirs(base_save_dir)
with open("urls.txt", 'r') as txt_file:
    for line in txt_file:
        line = line.strip()
        if line.startswith('#'):
            continue
        url = line
        urlsplit = url.split('/')
        for i in range(len(urlsplit)):
            if i == 0 or i == 1 or i == 2:
                continue
            if i == 3:
                save_path = dir + "\\" + urlsplit[i]
            save_path = save_path + "\\" + urlsplit[i]
        download_file(url, save_path)
