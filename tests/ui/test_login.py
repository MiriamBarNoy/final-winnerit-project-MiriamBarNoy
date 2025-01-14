import pytest
import re
from playwright.sync_api import sync_playwright, Browser, expect
from tests.conftest import base_url_ui
from tests.conftest import setup_browser
from pages.login_page import LoginPage
import allure


#data sets for login tests
fix_password = "secret_sauce"
login_success_data = [
    ('standard_user',fix_password),
    ('problem_user',fix_password),
    ('performance_glitch_user',fix_password),
    ('error_user',fix_password),
    ('visual_user',fix_password),
    ('will fail',fix_password)
              ]
login_error_data = [
    ('locked_out_user',fix_password,'Epic sadface: Sorry, this user has been locked out'),
    ('',fix_password,'Epic sadface: Username is required'),
    ('standard_user','','Epic sadface: Password is required'),
    ('error_user','not_correct','Epic sadface: Username and password do not match any user in this service'),
              ]
#successfull login tests that are transferred to next page
#1 test will fail here to see it on report
@allure.feature("Login")
@allure.story("Happy flow")
@allure.title("Success login from UI")
@pytest.mark.ui
@pytest.mark.parametrize("email,password",login_success_data)
def test_successful_logins(email,password,setup_browser,base_url_ui):
    this_page = setup_browser
    login_page = LoginPage(this_page)
    login_page.login(email, password)
    allure.attach(this_page.screenshot())
    assert this_page.url == f'{base_url_ui}inventory.html'

#unsuccsesful login attempts with correct error message
@allure.feature("Login")
@allure.story("Negative flow")
@allure.title("Login failures including relevant error validation")
@pytest.mark.ui
@pytest.mark.parametrize("email,password,error",login_error_data)
def test_unsuccessful_logins(email,password,error,setup_browser):
    this_page = setup_browser
    login_page = LoginPage(this_page)
    login_page.login(email, password)
    allure.attach(this_page.screenshot())
    expect(login_page.error).to_contain_text(error)

