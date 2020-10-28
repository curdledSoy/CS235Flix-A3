from flask import session
import os
import pytest


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/auth/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/auth/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/auth/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Username too short!'),
        ('test', '', b'Your password is required'),
        ('test', 'test',
         b"Your password must contain an uppercase letter, a lowercase letter, a digit and be at least 6 " \
         b"characters in length ",
         ),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/auth/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert 'username' in session


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'username' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data


def test_login_required_to_review(client):
    response = client.post('/movies/review')
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/movies/review?title=Moana&year=2016')

    response = client.post(
        '/movies/review',
        data={'review': 'Who needs quarantine?', 'rating': 3, 'movie_title': 'Moana', 'movie_year': 2016}
    )
    assert response.headers['Location'] == 'http://localhost/movies/?title=Moana&year=2016'


@pytest.mark.parametrize(('review', 'messages', 'rating'), (
        ('Who thinks Trump is a fuckwit?', (b'Your comment must not contain profanity'),6),
        ('Hey', (b'Your comment is too short'),5),
))
def test_review_with_invalid_input(client, auth, review, messages,rating):
    # Login a user.
    auth.login()

    # Attempt to review a movie
    response = client.post(
        'movies/review',
        data={'review': review, 'title': 'Moana', 'movie_year': 2016, 'movie_rating': rating}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_browse_movies_by_name(client):
    response = client.get('http://127.0.0.1:5000/browse/movies?character=2')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'2012' in response.data
    assert b'21 Jump Street' in response.data


def test_actors(client):
    response = client.get('http://127.0.0.1:5000/browse/actors?character=A')
    assert response.status_code == 200

    assert b'A.C. Peterson' in response.data

def test_directors(client):
    response = client.get('http://127.0.0.1:5000/browse/directors?character=A')
    assert response.status_code == 200
    assert b'Aamir Khan' in response.data

def test_genres(client):
    response = client.get('http://127.0.0.1:5000/browse/genres')
    assert response.status_code == 200

    assert b'Comedy' in response.data




