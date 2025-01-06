import pytest
import re
from playwright.sync_api import sync_playwright, Browser
from time import sleep

#base url for API tests
@pytest.fixture()
def base_url_api():
    return "https://reqres.in/api"

@pytest.fixture()
def setup_browser():
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        sleep(5)
        yield page