from fastapi import FastAPI
from starlette.responses import RedirectResponse, HTMLResponse

import hashlib
from enum import Enum
import time

import web_utils
from web_utils import BrowserType

from redis_collections import Dict
from redis import StrictRedis

conn = StrictRedis()
page_dict = Dict(redis=conn, writeback=True, key='SPYDERWEB__PAGE_DICT')

class FilterType(str, Enum):
    filter_param = "param"
    filter_regex = "regex"

app = FastAPI(title='SpyderWeb', version='0.3.0')

@app.get("/")
async def read_root():
    response = RedirectResponse(url='/docs')
    return response

@app.post("/page")
async def post_page(url: str, expiry: int = 3600, browser_type: BrowserType = 'firefox', force_update: bool = False):
    hashid = hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]
    if not hashid in page_dict or force_update:
        page_dict[hashid] = {
            'hash':hashid,
            'url':url, 
            'browser_type':browser_type,
            'expiry':expiry,
            'worker':None,
            'creation_time':int(time.time()),
            'last_update':None,
            'last_health_check':None
            }
    page_dict.sync()
    return hashid

@app.post("/{page_id}/filter")
async def post_filter(page_id: int, filter_str: str, filter_type: FilterType = 'param', frequency: int = None, expiry: int = None):
    return {'add_filter': settings}

@app.get("/get", response_class=HTMLResponse)
async def get(url: str, browser_type: BrowserType = 'firefox'):
    browser = web_utils.get_browser(url, browser_type)
    page_source = browser.page_source
    browser.quit()
    return page_source

@app.get("/show/all")
async def show_pages():
    return page_dict

@app.get("/show/{page_id}")
async def show_page(page_id: str):
    return page_dict.get(page_id,{})

@app.get("/show/{page_id}/filters")
async def show_page_filters(page_id: int):
    return {'list_filters': page_id}

@app.get("/show/{page_id}/{filter_id}")
async def show_page_filter(page_id: int, filter_id: int, start_time: int = None, end_time: int = None):
    return {'get': page_id}

@app.get("/delete/{page_id}")
async def delete_page(page_id: int, start_time: int, end_time: int = None):
    return {'delete_time': page_id}

@app.get("/delete/{page_id}/{filter_id}")
async def delete_page_filter(page_id: int, filter_id: int, start_time: int, end_time: int = None):
    return {'delete_time': page_id}

@app.get("/health")
async def health():
    try:
        r = {'healthy':conn.ping()}
    except:
        r = {'healthy':False}
    return r

