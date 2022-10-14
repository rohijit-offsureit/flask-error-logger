from flask.testing import FlaskClient


def test_404_rest(rest_client: FlaskClient):
    response = rest_client.get('/get-404')
    assert response.data == b'{\n  "error": "URL Not Found"\n}\n'
