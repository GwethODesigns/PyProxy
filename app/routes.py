from app import app, templates
from app.helper import *
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response, FileResponse, StreamingResponse
from PIL import Image
import requests_html, requests, io
from bs4 import BeautifulSoup as bs

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})

@app.get('/main/_rd', response_class=RedirectResponse)
def proxyRedirect(url: str = 'https://www.google.com'):
    url = url if url != '' else 'https://www.google.com'
    return RedirectResponse(f'/main/{url}')

@app.get('/main/_img/{url:path}', response_class=Response)
def ImageProxy(url: str):
    return CheckImages(url, requests_html.AsyncHTMLSession()) or RedirectResponse(f'/main/{url}')

@app.get('/main/_js/{url:path}')
def JavaScriptProxy(url: str):
    r = requests.get(url)
    return Response(r.content)

@app.get('/main/_css/{url:path}')
def CSSProxy(url: str):
    r = requests.get(url)
    return Response(r.content)

@app.get('/main/_txt/{url:path}')
def JavaScriptProxy(url: str):
    r = requests.get(url)
    return Response(r.content)

@app.get('/main/{url:path}', response_class=Response)
async def proxy(url: str):
    session = requests_html.AsyncHTMLSession()

    img = CheckImages(url, session)
    if img:
        return img

    # if url.endswith

    r = await session.get(url)

    await r.html.arender()
    soup = bs(r.text, "html.parser")

    
    soup = processSite(soup, url)

    return soup.prettify()