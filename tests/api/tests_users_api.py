import requests
import pytest
from assertpy import assert_that

from tests.conftest import base_url_api


users_data = [
              (1,'email','george.bluth@reqres.in'),
              (2,'first_name','Janet'),
              (7,'last_name','Lawson'),
              (9,'avatar',f'https://reqres.in/img/faces/9-image.jpg'),
              (8,'last_name','bla'),
              (1,'name','george')
              ]
#this will test that response code & data are as expected testing sample fields per few users
#2 tests will fail
@pytest.mark.parametrize("user_id,field,value",users_data)
def test_get_users(user_id,field,value, base_url_api):
    response = requests.get(f'{base_url_api}/users/{user_id}')
    assert response.status_code == 200
    assert response.reason == "OK"
    json_data = response.json()
    actual_value = json_data.get("data", {}) # this will access the data on json where above fields are
    for key in field.split('.'): #this will split the field string to a list of keys,e.g: "data.email", =['data', 'email']
        actual_value = actual_value.get(key, None)
        assert actual_value == value

#this will test that if user not found - correct response code is received with no crash
def test_get_users_not_found(base_url_api):
    response = requests.get(f'{base_url_api}/users/999')
    assert response.status_code == 404
    assert response.reason.upper() == "NOT FOUND"
    assert_that(response.json()).is_empty()

#this will test getting user list
def test_get_users_list(base_url_api):
    response = requests.get(f'{base_url_api}/users/')
    assert response.status_code == 200 # this asserts correct responce
    json_data = response.json()
    num_of_entries = int(json_data.get("per_page", {}))
    assert_that(json_data).is_length(num_of_entries) # this assert number of entries per page as expected
    first_user_json = requests.get(f'{base_url_api}/users/1').json().get("data", {})
    second_user_json = requests.get(f'{base_url_api}/users/2').json().get("data", {})
    first_entry = json_data["data"][0]
    second_entry = json_data["data"][1]
#This asserts data
    assert first_entry == first_user_json
    assert second_entry == second_user_json

def test_post_new_users():
    pass

def test_put_users():
    pass

def test_delete_users():
    pass

def test_get_resource():
    pass

def test_registration():
    pass

def test_login():
    pass



