from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='app/templates')

app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app import routes