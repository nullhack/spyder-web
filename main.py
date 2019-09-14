from fastapi import FastAPI
from starlette.responses import HTMLResponse

from selenium import webdriver    
from selenium.webdriver.firefox.options import Options
import hashlib
import json
from enum import Enum


class FilterType(str, Enum):
    filter_param = "param"
    filter_regex = "regex"

browser_dict = {}

#browser.quit()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/load")
def load(name: str):
    return {'load':'code'}

@app.get("/add_page")
def add_page(url: str, expiry: int = 3600):
    h = hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]
    if not h in browser_dict:
        options = Options()
        options.headless = True
        new_browser = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
        new_browser.get(url)
        browser_dict[h] = {'url':url, 'expiry':expiry, 'browser':new_browser}
    return h

@app.get("/list_pages")
def list_pages():
    return {k:browser_dict[k]['url'] for k in browser_dict.keys()}

@app.get("/{page_id}/get", response_class=HTMLResponse)
def add_filter(page_id: str):
    return browser_dict[page_id]['browser'].page_source

@app.get("/{page_id}/add_filter")
def add_filter(page_id: int, filter_str: str, filter_type: FilterType = 'param', frequency: int = None, expiry: int = None):
    return {'add_filter': settings}

@app.get("/{page_id}/list_filters")
def list_filters(page_id: int):
    return {'list_filters': page_id}

@app.get("/{page_id}/{filter_id}/get")
def get_data(page_id: int, filter_id: int, start_time: int = None, end_time: int = None):
    return {'get': page_id}

@app.get("/{page_id}/{filter_id}/delete")
def delete_data(page_id: int, filter_id: int, start_time: int, end_time: int = None):
    return {'delete_time': page_id}

@app.get("/health")
def health():
    return {'health': 'status'}

