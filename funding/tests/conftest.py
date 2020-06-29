import pytest
from flaskr import create_app
from flaskr.db import init_db
import mongomock


db = mongomock.MongoClient()['test']


# replace get_db method with one which uses mockdb
def fake_db():
    return db


@pytest.fixture(autouse=True)
def mocked_db(monkeypatch):
    monkeypatch.setattr('flaskr.db.get_db', fake_db)


@pytest.fixture
def app():
    # create the app
    app = create_app({
        'TESTING': True,
        'API_KEY': 'fake key'
    })

    # initialize the DB
    with app.app_context():
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()

