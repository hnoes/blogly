import pytest
from app import app
from models import db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client

def test_index_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.location == 'http://localhost/users'

def test_users_route(client):
    # test users
    user1 = User(first_name='John', last_name="Doe")
    user2 = User(first_name='Jane', last_name='Smith')
    db.session.add_all([user1, user2])
    db.session.commit()

    # Test the route that displays user details
    response = client.get('/users')
    assert response.status_code == 200
    assert b'John Doe' in response.data
    assert b'Jane Smith' in response.data
    assert b'Image URL: test_image.jpg' in response.data

def test_new_user_route