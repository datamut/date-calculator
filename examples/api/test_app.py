from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_calculator():
    response = client.request('POST', '/calculator', json={
        'first_day': '28/2/2000',
        'last_day': '1/03/2000'
    })
    assert response.status_code == 200
    assert response.json()['days'] == 1


def test_calculator_error():
    response = client.request('POST', '/calculator', json={
        'first_day': '30/2/2000',
        'last_day': '1/03/2000'
    })
    assert response.status_code == 500

    response = client.request('POST', '/calculator', json={
        'first_day': '28/2/2000',
        'last_day': '1/03/2000',
        'fmt': '%Y-%m-%d'
    })
    assert response.status_code == 500
