import pytest
from src.app import app


@pytest.fixture
def app_context():
    with app.app_context():
        yield


def some_test(app_context):