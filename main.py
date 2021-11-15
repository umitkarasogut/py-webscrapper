import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import os.path
from os import path
from colorama import Fore
import urllib.request

print("Example Url : https://www.google.com")
url = input("Enter site url  : ")

session = requests.Session()
session.headers[
    "User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
html = session.get(url).content
soup = bs(html, "html.parser")

script_files = []
for script in soup.find_all("script"):
    if script.attrs.get("src"):
        script_url = urljoin(url, script.attrs.get("src"))
        script_files.append(script_url)
        script['src'] = "assets/js/" + script_url.split("/")[-1]

css_files = []
for css in soup.find_all("link"):
    if css.attrs.get("href"):
        css_url = urljoin(url, css.attrs.get("href"))
        css_files.append(css_url)
        css['href'] = "assets/css/" + css_url.split("/")[-1]

image_files = []
for image in soup.find_all("img"):
    if image.attrs.get("src"):
        image_url = urljoin(url, image.attrs.get("src"))
        image_files.append(image_url)
        image['src'] = "assets/images/" + image_url.split("/")[-1]

if not path.exists("site_content"):
    os.mkdir("site_content")

if not path.exists("site_content/assets"):
    os.mkdir("site_content/assets")

if not path.exists("site_content/assets/js"):
    os.mkdir("site_content/assets/js")

if not path.exists("site_content/assets/images"):
    os.mkdir("site_content/assets/images")

if not path.exists("site_content/assets/css"):
    os.mkdir("site_content/assets/css")

html = html.decode("utf-8")

for file in script_files:
    request = session.get(file)
    file_domain = file.split("/")[2]
    request_domain = url.split("/")[2]
    if file_domain == request_domain:
        if request.status_code == 200:
            file_content = request.text
            file_name = file.split("/")[-1]
            if file_name != "":
                f = open("./site_content/assets/js/" + file_name, "a")
                f.write(str(file_content))
                f.close()
        else:
            print("Server error status code : ", request.status_code, "File : ", file)

for file in css_files:
    request = session.get(file)
    file_domain = file.split("/")[2]
    request_domain = url.split("/")[2]
    if file_domain == request_domain:
        if request.status_code == 200:
            file_content = request.text
            file_name = file.split("/")[-1]
            if file_name != "":
                f = open("./site_content/assets/css/" + file_name, "a")
                f.write(str(file_content))
                f.close()
        else:
            print("Server error status code : ", request.status_code, "File : ", file)

for file in image_files:
    file_name = file.split("/")[-1]
    urllib.request.urlretrieve(file, "./site_content/assets/images/" + file_name)

f = open("./site_content/index.html", "a")
f.write(str(soup))
f.close()

print(Fore.GREEN + "Site exported successfully")
print("HTML File : site_content/index.html")
print("Js Assets : site_content/assets/js")
print("Css Assets : site_content/assets/css")
print("Image Assets : site_content/assets/images")
