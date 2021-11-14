import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import os
import os.path
from os import path
import re

url = "http://jbm.com.tr"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
html = session.get(url).content
soup = bs(html, "html.parser")

script_files = []
for script in soup.find_all("script"):
    if script.attrs.get("src"):
        script_url = urljoin(url, script.attrs.get("src"))
        script_files.append(script_url)

css_files = []
for css in soup.find_all("link"):
    if css.attrs.get("href"):
        css_url = urljoin(url, css.attrs.get("href"))
        css_files.append(css_url)

if not path.exists("site_content"):
    os.mkdir("site_content")

for file in script_files:
    request = session.get(file)
    if request.status_code == 200:
        file_content = request.content
        d = request.headers['content-disposition']
        file_name = re.findall("filename=(.+)", d)[0]
    else:
        print("Server error status code : ", request.status_code)

