"""Module for Pytest Configuration"""

# system imports
import os
from os import getenv, environ
from unittest.mock import Mock

# third party imports
import pytest
from faker import Faker

# local import
from api.features import User
from settings import db, create_app

fake = Faker()
TEST_ENV = 'testing'
environ['FLASK_ENV'] = TEST_ENV
ENV = getenv('FLASK_ENV')
print('ENV=', ENV)

@pytest.fixture(scope='session')
def flask_app():
    """Create a flask application instance for Pytest.
	Returns:
		Object: Flask application object
	"""

    # create an application instance
    _app = create_app(ENV)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    # yield the application context for making requests
    yield _app

    ctx.pop()


@pytest.fixture
def client(flask_app):
    """Setup client for making http requests, this will be run on every
	test function.
	Args:
		flask_app (func): Flask application instance
	Returns:
		Object: flask application client instance
	"""

    # initialize the flask test_client from the flask application instance
    client = flask_app.test_client()

    yield client


@pytest.fixture
def init_db(flask_app):
    """Fixture to initialize the database"""
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.close()
        db.drop_all()


@pytest.fixture(scope='function')
def saved_user_model(init_db):
    user_data = {
        "username": fake.first_name()[:20],
        "email": fake.email(),
        "password": fake.password(),
    }
    user = User(**user_data)
    user.save()

    return user
