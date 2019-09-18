from fastapi import FastAPI
from starlette.responses import RedirectResponse

from selenium import webdriver    
from selenium.webdriver.firefox.options import Options
import hashlib
from enum import Enum
import time

from redis_collections import Dict
from redis import StrictRedis

conn = StrictRedis()
page_dict = Dict(redis=conn, writeback=True, key='SPYDERWEB__PAGE_DICT')

class FilterType(str, Enum):
    filter_param = "param"
    filter_regex = "regex"

class BrowserType(str, Enum):
    browser_firefox = "firefox"
    browser_chrome = "chrome"

app = FastAPI(title='SpyderWeb', version='0.3.0')

@app.get("/")
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

@app.post("/page")
async def post_page(url: str, expiry: int = 3600, browser_type: BrowserType = 'firefox', force_update: bool = False):
    h = hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]
    if not h in page_dict or force_update:
        page_dict[h] = {
            'hash':h,
            'url':url, 
            'browser_type':browser_type,
            'expiry':expiry,
            'worker':None,
            'creation_time':int(time.time()),
            'last_update':None,
            'last_health_check':None
            }
    page_dict.sync()
    return h

@app.get("/list_pages")
async def list_pages():
    return page_dict

@app.get("/{page_id}/get")
async def get_page(page_id: str):
    return page_dict.get(page_id,{})

@app.post("/{page_id}/filter")
async def post_filter(page_id: int, filter_str: str, filter_type: FilterType = 'param', frequency: int = None, expiry: int = None):
    return {'add_filter': settings}

@app.get("/{page_id}/list_filters")
async def list_filters(page_id: int):
    return {'list_filters': page_id}

@app.get("/{page_id}/{filter_id}/get")
async def get_data(page_id: int, filter_id: int, start_time: int = None, end_time: int = None):
    return {'get': page_id}

@app.get("/{page_id}/{filter_id}/delete")
async def delete_data(page_id: int, filter_id: int, start_time: int, end_time: int = None):
    return {'delete_time': page_id}

@app.get("/health")
async def health():
    try:
        return {'healthy':conn.ping()}
    except:
        return {'healthy':False}

