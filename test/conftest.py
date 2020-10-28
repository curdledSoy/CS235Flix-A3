import os

import pytest


from cs235flix import create_app, MemoryRepository
from cs235flix.adapters import memory_repository

TEST_DATA_PATH_MEMORY = os.path.join('/Users/tombrittenden/OneDrive - The University of Auckland/2020/Semester 2/COMPSCI 235/CS235Flix/CS325FLIX-A2', 'test', 'data', 'memory')


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH_MEMORY, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'WTF_CSRF_ENABLED': False,                       # test_client will not send a CSRF token, so disable validation.
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='admin'):
        return self._client.post(
            'auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)