import json
import urllib
import urllib.request
from urllib.parse import parse_qs

import requests
from PIL import Image
from bs4 import BeautifulSoup
from tqdm import tqdm

from image_window import ImageWindow
from download_img import fetch_imgs


def is_captcha(content):
    soup = BeautifulSoup(content, 'html.parser')

    captcha_wrapper = soup.findAll("div", {"class": "captcha-wrapper"})
    form_error_no = soup.findAll("form", {"class": "form_error_no"})

    #print("captcha_wrapper", captcha_wrapper)
    #print("form_error_no", form_error_no)
    if captcha_wrapper or form_error_no:
        return True

    return False


def send_captcha_code(key, retpath, rep):
    url = "http://yandex.ru/checkcaptcha"

    response = requests.get(url,
                            headers={"User-Agent": "Alcatel-BF5/1.0 UP.Browser/5.0"},
                            allow_redirects=True,
                            params={"key": key, "retpath": retpath, "rep": rep})

    return response.content.decode('utf-8')


def parse_captcha_page(content):
    # parse screen captcha
    soup = BeautifulSoup(content, 'html.parser')

    elem = soup.findAll("input", {"class": "form__key"})
    key = elem[0]['value']

    elem = soup.findAll("input", {"class": "form__retpath"})
    retpath = elem[0]['value']

    elem = soup.findAll("div", {"class": "captcha__image"})
    src_captcha_image = elem[0].img["src"]

    return key, retpath, src_captcha_image


def get_captcha_image(src_captcha_image):
    # create a file-like object from the url
    file = urllib.request.urlopen(src_captcha_image)
    return Image.open(file)


def get_images_page(page=None, query=None):
    url_p = "https://yandex.ru/images/smart/search"

    response = requests.get(url_p,
                            headers={"User-Agent": "Alcatel-BF5/1.0 UP.Browser/5.0"},
                            params={"p": page, "text": query, "rpt": "image_smart"})
    return response.content.decode('utf-8')


def parse_page_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    a_list = soup.findAll("a", {"class": "serp-item"})

    link_list = list()
    for query in a_list:
        arr_qs = parse_qs(query['href'])
        link_list.append(arr_qs['img_url'][0])
    return link_list


query = "венегрет"
start_page = 160
pages = 162

page_links = []
for i in tqdm(range(start_page, pages)):
    content = get_images_page(page=i, query=query)

    while is_captcha(content):
        print("Captcha entered ", i)
        key, retpath, src_captcha_image = parse_captcha_page(content)

        image = get_captcha_image(src_captcha_image)

        img_w = ImageWindow(image)
        rep = img_w.get_captcha_text()

        content = send_captcha_code(key, retpath, rep)

    links = parse_page_links(content)
    page_links.append(links)

    fetch_imgs(links)

    with open('img_links.json', 'w') as outfile:
        json.dump(page_links, outfile)
