from app import app, templates
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response, StreamingResponse
import requests_html
from bs4 import BeautifulSoup as bs

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})


@app.get('/main/{url:path}', response_class=Response)
async def proxy(url: str):
    session = requests_html.AsyncHTMLSession()
    r = await session.get(url)
    if any(url.endswith(f'.{ext}') for ext in ['png', 'jpg', 'jpeg', 'gif', 'tif', 'tiff', 'svg', 'bmp']):
        return Response(content=r.content, media_type='image')
    imgs = r.html.find('img')
    for img in imgs:
        img.src = '/main/' + url + '/'
    await r.html.arender()
    return r.text