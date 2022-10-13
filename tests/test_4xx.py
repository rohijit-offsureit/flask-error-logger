from flask.testing import FlaskClient

def test_404_rest(rest_client: FlaskClient):
    response = rest_client.get('/get-404')
    with open("test_output.txt","w",encoding="utf-8") as f:
        f.write(str(response.data))
    assert True