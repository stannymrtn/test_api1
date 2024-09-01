import json
import requests
from jsonschema import validate
from utils.resource import path


def test_create_user(base_url):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }

    response = requests.post(base_url + '/api/users', data=payload)

    assert response.status_code == 201
    assert response.json()['name'] == "morpheus"
    assert response.json()['job'] == "leader"

    schema = path('post_create_user.json')

    with open(schema) as file:
        f = file.read()
        validate(response.json(), schema=json.loads(f))


def test_register_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(base_url + '/api/register', data=payload)
    assert response.json()['token']


def test_login_successful(base_url):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }
    response = requests.post(base_url + '/api/login', data=payload)
    assert 'token' in response.json()

    schema = path('post_login_user.json')

    with open(schema) as file:
        f = file.read()
        validate(response.json(), schema=json.loads(f))


def test_login_unsuccessful(base_url):
    response = requests.post(base_url + '/api/login', data={"email": "peter@klaven"})
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_delete(base_url):
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = requests.post(base_url + '/api/users', data=payload)
    id = response.json()['id']
    delete = requests.delete(base_url + '/api/users/' + id)
    assert delete.status_code == 204
    assert delete.text == ''