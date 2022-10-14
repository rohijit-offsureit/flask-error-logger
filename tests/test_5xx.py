import json
from flask.testing import FlaskClient


def test_500_rest(rest_client: FlaskClient):
    response = rest_client.get('/get-500')
    data = json.loads(response.data.decode("utf-8"))
    assert "error" in data
