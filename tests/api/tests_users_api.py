import requests
import pytest
from assertpy import assert_that
from tests.conftest import base_url_api
from faker import Faker

#this will define the users end point
@pytest.fixture()
def users_end_point(base_url_api):
    return f'{base_url_api}/users'

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
def test_get_users(user_id,field,value, users_end_point):
    response = requests.get(f'{users_end_point}/{user_id}')
    assert response.status_code == 200
    assert response.reason == "OK"
    json_data = response.json()
    actual_value = json_data.get("data", {}) # this will access the data on json where above fields are
    for key in field.split('.'): #this will split the field string to a list of keys,e.g: "data.email", =['data', 'email']
        actual_value = actual_value.get(key, None)
        assert actual_value == value

#this will test that if user not found - correct response code is received with no crash
def test_get_users_not_found(users_end_point):
    response = requests.get(f'{users_end_point}/999')
    assert response.status_code == 404
    assert response.reason.upper() == "NOT FOUND"
    assert_that(response.json()).is_empty()

#this will test getting user list
def test_get_users_list(users_end_point):
    response = requests.get(users_end_point)
    assert response.status_code == 200 # this asserts correct responce
    json_data = response.json()
    num_of_entries = int(json_data.get("per_page", {}))
    assert_that(json_data).is_length(num_of_entries) # this assert number of entries per page as expected
    first_user_json = requests.get(f'{users_end_point}/1').json().get("data", {})
    second_user_json = requests.get(f'{users_end_point}/2').json().get("data", {})
    first_entry = json_data["data"][0]
    second_entry = json_data["data"][1]
#This asserts data
    assert first_entry == first_user_json
    assert second_entry == second_user_json

def test_post_new_users(users_end_point):
     name = Faker().name() #This will create a fake user to use on creation
     email = Faker().email() #This will create a fake email to use on creation
     job = Faker().job() #This will create a jb to use on creation
     new_user = {"name": name, "email": email, "job": job}
     response = requests.post(f'{users_end_point}/', json=new_user) #creation request
     assert response.status_code == 201
     assert response.reason.upper() == "CREATED"
     assert 'id' in response.json()
     assert response.json()['name'] == name
     assert response.json()['email'] == email
     assert response.json()['job'] == job

def test_put_users(users_end_point):
    name = Faker().name()
    email = Faker().email()
    update_user = {"name": name, "email": email}
    response = requests.put(f'{users_end_point}/2', json=update_user)
    assert response.status_code == 200
    assert response.reason.upper() == "OK"
    assert 'updatedAt' in response.json()
    assert response.json()['name'] == name
    assert response.json()['email'] == email

def test_delete_users(users_end_point):
    response = requests.delete(f'{users_end_point}/2')
    assert response.status_code == 204
    assert response.reason.upper() == "NO CONTENT"


def test_registration():
    pass

def test_login():
    pass



