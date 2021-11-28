import pytest


@pytest.fixture
def room_input():
    return {
        'description': 'Double room',
        'price': 100
    }
