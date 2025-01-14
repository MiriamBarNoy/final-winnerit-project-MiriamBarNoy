import allure
import pytest
from playwright.sync_api import sync_playwright, Browser
from time import sleep

#base url for API tests
@pytest.fixture()
def base_url_api():
    with allure.step("navigate to base page for api tests:"):
        return "https://reqres.in/api"

#base url for UI tests
@pytest.fixture()
def base_url_ui():
    with allure.step("navigate to base page for ui tests:"):
        return "https://www.saucedemo.com/"

#set up browser for UI tests
@pytest.fixture()
def setup_browser(base_url_ui):
    with allure.step("define browser setup for ui tests:"):
        with sync_playwright() as p:
            browser: Browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(base_url_ui)
            yield page