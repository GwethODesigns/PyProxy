from bs4 import BeautifulSoup

def find_list_resources (tag: str, attribute: str, soup: BeautifulSoup):
   list = {}
   for x in soup.findAll(tag):
       try:
            _ = x[attribute]
            list[x] = attribute
       except KeyError:
           pass
    
   return list

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

    return srcs


def sterilize_url(url: str) -> str:

    if url.startswith('http://'):
        url = url if url.startswith('http://www.') else ('http://www.' + url[7:])

    if url.startswith('https://'):
        url = url if url.startswith('https://www.') else ('https://www.' + url[8:])
        
    url = url if url[-1] != "/" else url[:-1]

    return url