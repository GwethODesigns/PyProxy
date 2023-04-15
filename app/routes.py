from app import app, templates
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('main.html', {'request': request})
