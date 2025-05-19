import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from app import app as flask_app  # reference: https://flask.palletsprojects.com/en/2.3.x/api/#flask.Flask.test_client
from flask import session
 
#provide a test client with a mock user session
@pytest.fixture
def client():
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        #simulates a logged-in user using session_transaction
        # reference: https://flask.palletsprojects.com/en/2.3.x/api/#flask.testing.FlaskClient.session_transaction
        with client.session_transaction() as sess:
            sess['user'] = {'email': 'testuser@example.com'}
        yield client

#testing the /api/comments post route
def test_post_comment(client):
    #send a comment with a mock articleId and comment text
    response = client.post('/api/comments', json={
        "articleId": "test-article-id",
        "text": "This is a test comment"
    })

    assert response.status_code == 201

    # check that the response has the correct data
    data = response.get_json()
    assert data['articleId'] == "test-article-id"
    assert data['text'] == "This is a test comment"
    assert data['user'] == "testuser@example.com"
