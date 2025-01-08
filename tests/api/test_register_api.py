import requests
import pytest
from tests.conftest import base_url_api
from faker import Faker

#this will define the resource end point
@pytest.fixture()
def register_end_point(base_url_api):
    return f'{base_url_api}/register'

#This will test successful registration with correct response code and json
@pytest.mark.api
def test_successful_registration(register_end_point):
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    registration = {"email": email, "password": password}
    response = requests.post(f'{register_end_point}/', json=registration)  # creation request
    assert response.status_code == 200
    assert response.reason.upper() == "OK"
    assert 'id' in response.json()
    assert 'token' in response.json()

registration_errors = [
              (Faker().email(),Faker().password(),'Note: Only defined users succeed registration'),
              ('eve.holt@reqres.in','','Missing password'),
              ]
#This will test 2 unsuccessful registration cases with correct error message
@pytest.mark.parametrize("email,password,code_reason",registration_errors)
@pytest.mark.api
def test_unsuccessful_registration(email,password,code_reason, register_end_point):
    response = requests.get(f'{register_end_point}/')
    registration = {"email": email, "password": password}
    response = requests.post(f'{register_end_point}/', json=registration)
    json_data = response.json()
    assert response.status_code == 400
    assert json_data["error"] == code_reason

