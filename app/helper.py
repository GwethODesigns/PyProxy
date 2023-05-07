from bs4 import BeautifulSoup
from fastapi.responses import HTMLResponse, RedirectResponse, Response, FileResponse, StreamingResponse
from PIL import Image
import requests_html, requests, io

def find_list_resources (tag: str, attribute: str, soup: BeautifulSoup):
   list = {}
   for x in soup.findAll(tag):
       try:
            _ = x[attribute]
            list[x] = attribute
       except KeyError:
           pass
    
   return list


def get_host(url: str) -> str:

    if url.startswith('http://'):
        url = url if url.startswith('http://www.') else ('http://www.' + url[7:])

    if url.startswith('https://'):
        url = url if url.startswith('https://www.') else ('https://www.' + url[8:])
        
    url = url if url[-1] != "/" else url[:-1]

    url = '/'.join(url.split('/')[:3])

    return url


def processSite(soup: BeautifulSoup, url: str):
    # IMG SRC
    imgs = find_list_resources('img', 'src', soup)
    for img, _ in imgs.items():
        if img["src"].startswith("data:"):
            continue

        if img["src"].startswith('https://') or img["src"].startswith('http://'):
            img["src"] = f'/main/_img/{img["src"]}'
        else:
            img["src"] = f'/main/_img/{get_host(url)}{img["src"]}'

    # IMG SRCSET
    for item in soup.find_all('img'):
        if item.get('srcset') != None:
            srcset = item['srcset'].split(',')
            for i, src in enumerate(srcset):
                if src.startswith('https://') or src.startswith('http://'):
                    srcset[i] = f'/main/_img/{src}'
                else:
                    srcset[i] = f'/main/_img/{get_host(url)}{src}'
            item['srcset'] = ', '.join(srcset)

    # JS SRC
    scripts = find_list_resources('script', 'src', soup)
    for script, _ in scripts.items():
        if script["src"].startswith('https://') or script["src"].startswith('http://'):
            script["src"] = f'/main/_js/{script["src"]}'
        else:
            script["src"] = f'/main/_js/{get_host(url)}{script["src"]}'

    # LINK HREF
    links = find_list_resources('link', 'href', soup)
    for link, _ in links.items():

        if link.get('as') == 'script' and link['href'].endswith('.js'):
            linkType = 'js'
        elif link['href'].endswith('.css') and 'stylesheet' in link.get('rel'):
            linkType = 'css'
        elif 'icon' in link.get('rel'):
            linkType = 'img'
        else:
            linkType = 'txt'
        
        if link["href"].startswith('https://') or link["href"].startswith('http://'):
            link["href"] = f'/main/_{linkType}/{link["href"]}'
        else:
            link["href"] = f'/main/_{linkType}/{get_host(url)}{link["href"]}'

    return soup
    


def get_sources(soup: BeautifulSoup):
    srcs = {}
    srcs.update(find_list_resources('img',"src",soup))
    srcs.update(find_list_resources('script',"src",soup))
    srcs.update(find_list_resources("link","href",soup))
    srcs.update(find_list_resources("video","src",soup))
    srcs.update(find_list_resources("audio","src",soup))
    srcs.update(find_list_resources("iframe","src",soup))
    srcs.update(find_list_resources("embed","src",soup))
    srcs.update(find_list_resources("object","data",soup))
    srcs.update(find_list_resources("source","src",soup))
    srcs.update(find_list_resources("a","href",soup))

    return srcs



def CheckImages(url, session):
    if url.endswith('.png'):
        im = Image.open(requests.get(url, stream=True).raw)
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return Response(content=img_byte_arr, media_type="image/png")

    if url.endswith('.gif'):
        img_raw = requests.get(url, stream=True).content
        byte_io = io.BytesIO(img_raw)
        return StreamingResponse(byte_io, media_type='image/gif')