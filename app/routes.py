from app import app, templates
from app.helper import get_sources, sterilize_url
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response, FileResponse
from PIL import Image
import requests_html, requests, io
from bs4 import BeautifulSoup as bs

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})

@app.get('/main')
def proxyRedirect(url: str = 'https://www.google.com'):
    return RedirectResponse(f'/main/{url}')

@app.get('/main/{url:path}', response_class=Response)
async def proxy(url: str):
    session = requests_html.AsyncHTMLSession()

    if url.endswith('.png'):
        im = Image.open(requests.get(url, stream=True).raw)
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return Response(content=img_byte_arr, media_type="image/png")

    r = await session.get(url)

    await r.html.arender()
    soup = bs(r.text, "html.parser")
    
    srcs = get_sources(soup)

    for tag, attr in srcs.items():
        if tag[attr].startswith("data:"):
            continue

        if tag[attr].startswith('https://') or tag[attr].startswith('http://'):
            tag[attr] = f'/main/{tag[attr]}'
        else:
            tag[attr] = f'/main/{sterilize_url(url)}{tag[attr]}'

    for item in soup.find_all('img'):
        if item.get('srcset') != None:
            item['srcset'] = ', '.join(['/main/' + sterilize_url(url) + i for i in item['srcset'].split(', ')])
    
    return soup.prettify()