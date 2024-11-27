import pytest
from punchline_interfaces import ChuckNorrisServiceInterface

from app import create_app, db
from app.models import Joke


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def mocked_service(mocker):
    return mocker.patch.object(ChuckNorrisServiceInterface, "get_instance", autospec=True)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture
def joke():
    joke = Joke(value="Chuck Norris can divide by zero", categories=["nerdy"])
    db.session.add(joke)
    db.session.commit()
    return joke