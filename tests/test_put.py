import json
import requests
from jsonschema import validate
from utils.resource import path


def test_update(base_url):
    payload_post = {
        "name": "morpheus",
        "job": "leader"
    }
    payload_update = {
        "name": "Timur",
        "job": "QA"
    }
    response = requests.post(base_url + '/api/users', data=payload_post)
    id = response.json()['id']
    update = requests.put(base_url + '/api/users/' + id, data=payload_update)
    assert update.status_code == 200
    assert update.json()['name'] == "Timur"
    assert update.json()['job'] == "QA"
    schema = path('put_user.json')

    with open(schema) as file:
        f = file.read()
        validate(update.json(), schema=json.loads(f))
