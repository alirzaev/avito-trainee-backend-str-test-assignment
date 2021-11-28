import pytest


@pytest.fixture
def room_input():
    return {
        'description': 'Double room',
        'price': 100
    }


@pytest.fixture
def booking_input():
    return {
        'begin_date': '2021-01-01',
        'end_date': '2021-01-07',
        'room_id': 1
    }
