import allure
import requests
import pytest
from assertpy import assert_that
from tests.conftest import base_url_api


#this will define the resource end point
@pytest.fixture()
def resource_end_point(base_url_api):
    with allure.step("navigate to resources page:"):
       return f'{base_url_api}/unknown'

resource_data = [
              (1,'name','cerulean'),
              (2,'year',2001),
              (7,'color','#DECDBE'),
              (9,'pantone_value','18-3943'),
              (8,'year','bla'),
              (1,'name','george')
              ]
#this will test that response code & data are as expected testing sample fields per few resources
#2 tests will fail
@pytest.mark.api
@pytest.mark.parametrize("resource_id,field,value",resource_data)
@allure.feature("API resource tests")
@allure.story("get resource by ID")
def test_get_specific_resource(resource_id,field,value,resource_end_point):
    response = requests.get(f'{resource_end_point}/{resource_id}')
    assert response.status_code == 200
    assert response.reason == "OK"
    json_data = response.json()
    actual_value = json_data.get("data", {})  # this will access the data on json where above fields are
    for key in field.split(
            '.'):  # this will split the field string to a list of keys,e.g: "data.email", =['data', 'email']
        actual_value = actual_value.get(key, None)
        assert actual_value == value

#this will test getting resource list
@allure.feature("API resource tests")
@allure.story("get resource list")
@pytest.mark.api
def test_get_resource_list(resource_end_point):
    response = requests.get(resource_end_point)
    assert response.status_code == 200  # this asserts correct response
    json_data = response.json()
    num_of_entries = int(json_data.get("per_page", {}))
    assert_that(json_data).is_length(num_of_entries)  # this asserts number of entries per page as expected
    first_resource = requests.get(f'{resource_end_point}/1').json().get("data", {})
    second_resource = requests.get(f'{resource_end_point}/2').json().get("data", {})
    first_entry = json_data["data"][0]
    second_entry = json_data["data"][1]
    # This asserts data
    assert first_entry == first_resource
    assert second_entry == second_resource

#this will test resource not found
@pytest.mark.api
@allure.feature("API resource tests")
@allure.story("resource not found")
def test_resource_not_found(resource_end_point):
    response = requests.get(f'{resource_end_point}/999')
    assert response.status_code == 404
    assert response.reason.upper() == "NOT FOUND"
    assert_that(response.json()).is_empty()