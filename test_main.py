from urlabridge import create_app


def test_abridge(client):
    response = client.get("/")
    assert b"Abridge" in response.data
