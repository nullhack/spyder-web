from selenium import webdriver    
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from enum import Enum

class BrowserType(str, Enum):
    browser_firefox = "firefox"
    browser_chrome = "chrome"


def get_firefox_browser(url:str = None, window_size:tuple = (1920,1080), user_agent:str = None):
    options = FirefoxOptions()
    options.headless = True
    profile = webdriver.FirefoxProfile()
    if user_agent: profile.set_preference("general.useragent.override", user_agent)
    browser = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=r'/usr/bin/geckodriver')
    if url: browser.get(url)
    if window_size: browser.set_window_size(*window_size)
    return browser

def get_chrome_browser(url:str = None, window_size:tuple = (1920,1080), user_agent:str = None):
    options = ChromeOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    if user_agent: options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(options=options, executable_path=r'/usr/bin/chromedriver')
    if url: browser.get(url)
    if window_size: browser.set_window_size(*window_size)
    return browser

def get_browser(url:str = None, window_size:tuple = (1920,1080), browser_type:BrowserType = 'firefox', user_agent:str = None):
    browser = None
    if browser_type == 'firefox': browser = get_firefox_browser(url, window_size, user_agent)
    elif browser_type == 'chrome': browser = get_chrome_browser(url, window_size, user_agent)
    return browser

user_agent = {
        'firefox':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'edge':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'chrome':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'safari':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'xbox one s':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'google bot':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'bing bot':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'samsung galaxy tab s3':'Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
        'microsoft lumia 950':'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058',
        'apple iphone xr':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
        'samsung galaxy s9':'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'apple iphone 8':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
        }
