import json

from project import db 
from project.api.models import User
from project.tests.utils import add_user,recreate_db

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username':'wanyaland',
            'email':'wanyaland@gmail.com'
        }),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'wanyaland@gmail.com was added' in data['message']
    assert 'success' in data['status']

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data = json.dumps({}),
        content_type = 'application/json'
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Invalid Payload' in data['message']
    assert 'fail' in data['status']

def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data = json.dumps({
            'email':'harry@gmail.com'
        }),
        content_type = 'application/json'
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Invalid Payload' in data['message']
    assert 'fail' in data['status']

def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data = json.dumps({
            'username':'wanyaland',
            'email' : 'wanayaland@gmail.com',
        }),
        content_type = 'application/json'
    )

    resp = client.post (
        '/users',
        data = json.dumps({
            'username':'wanyaland',
            'email': 'wanyaland@gmail.com'
        }),
        content_type = 'application/json'
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists' in data['message']
    assert 'fail' in data['status']

def test_single_user(test_app, test_database):
    user = User(username='wanyaland', email = 'wanyaland@gmail.com')
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'wanyaland' in data['data']['username']
    assert 'wanyaland@gmail.com' in data['data']['email']
    assert 'success' in data['status']

def test_get_user_no_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/blah')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User does not exist' in data['message']
    assert 'fail' in data['status']

def test_get_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('/users/888')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User does not exist' in data ['message']
    assert 'fail' in data['status']

def test_get_users(test_app , test_database):
    recreate_db()
    client = test_app.test_client()
    add_user('wanyaland','wanyaland@gmail.com')
    add_user('nachwera','nachwera@gmail.com')
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data['data']['users']) == 2
    assert 'wanyaland' in data['data']['users'][0]['username']
    assert 'wanyaland@gmail.com' in data['data']['users'][0]['email']
    assert 'nachwera' in data['data']['users'][1]['username']
    assert 'nachwera@gmail' in data['data']['users'][1]['email']



