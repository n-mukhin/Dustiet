import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Anime Lounge Service' in response.data

def test_register(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'user_id' in response.get_json()

def test_login_unauthorized(client):
    response = client.post('/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['status'] == 'unauthorized'
