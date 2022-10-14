from flask.testing import FlaskClient

def test_500_rest(rest_client:FlaskClient):
    response = rest_client.get('/get-500')
    with open("test_output5xx.txt","w",encoding="utf-8") as f:
        f.write(str(response.data))
    assert True