import pytest
from playwright.sync_api import sync_playwright, Browser
from time import sleep

#base url for API tests
@pytest.fixture()
def base_url_api():
    return "https://reqres.in/api"

#base url for UI tests
@pytest.fixture()
def base_url_ui():
    return "https://www.saucedemo.com/"

#set up browser for UI tests
@pytest.fixture()
def setup_browser(base_url_ui):
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(base_url_ui)
        yield page