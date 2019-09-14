from fastapi import FastAPI
from starlette.responses import HTMLResponse

from selenium import webdriver    
from selenium.webdriver.firefox.options import Options
         
options = Options()
options.headless = True
browser = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')    

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/get", response_class=HTMLResponse)
def read_page(q: str):
    browser.get(q) 
    print(browser.title)                                
    return browser.page_source

