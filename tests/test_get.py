import json
import requests
from jsonschema import validate
from utils.resource import path


def test_return_single_user(base_url):
    response = requests.get(
        base_url + '/api/users/1'
    )
    email = "george.bluth@reqres.in"
    body = response.json()
    schema = path('get_user.json')

    assert response.json()['data']['email'] == email
    with open(schema) as file:
        f = file.read()
        validate(body, schema=json.loads(f))


def test_return_list_users(base_url):
    response = requests.get(base_url + '/api/users?page=2')

    body = response.json()
    schema = path('get_users.json')

    assert response.status_code == 200
    with open(schema) as file:
        f = file.read()
        validate(body, schema=json.loads(f))


def test_single_resource_not_found(base_url):
    response = requests.get(base_url + '/api/unknown/22')
    assert response.status_code == 404
