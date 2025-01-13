import requests
import pytest
from tests.conftest import base_url_api
from faker import Faker
import allure

#this will define the login end point

@pytest.fixture()
def login_end_point(base_url_api):
    with allure.step("navigate to login page:"):
        return f'{base_url_api}/login'

#This will test successful login
@pytest.mark.api
@allure.feature("API login tests")
@allure.story("successful login")
@allure.title("successful login test")
def test_successful_login(login_end_point):
    email = 'eve.holt@reqres.in'
    password = 'cityslicka'
    login = {"email": email, "password": password}
    response = requests.post(f'{login_end_point}/', json=login)  # creation request
    assert response.status_code == 200
    assert response.reason.upper() == "OK"
    assert 'token' in response.json()

login_errors = [
    (Faker().email(),Faker().password(),'user not found'),
    ('eve.holt@reqres.in','','Missing password'),
              ]
#This will test 2 unsuccessful login cases with correct error message
@allure.feature("API login tests")
@allure.story("failure login")
@allure.title("Login failures tests including relevant errors")
@pytest.mark.parametrize("email,password,code_reason",login_errors)
@pytest.mark.api
def test_unsuccessful_login(email,password,code_reason, login_end_point):
    registration = {"email": email, "password": password}
    response = requests.post(f'{login_end_point}/', json=registration)
    json_data = response.json()
    assert response.status_code == 400
    assert json_data["error"] == code_reason

