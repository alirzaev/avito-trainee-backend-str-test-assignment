import datetime

import pytest

from rest_framework.reverse import reverse

from api.models import Booking, Room


@pytest.mark.django_db
def test_booking_create_success(client, room_input, booking_input):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    response = client.post(reverse('booking-list'), data=input_data)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data

    booking = Booking.objects.get(pk=data['id'])
    assert booking.begin_date == datetime.date.fromisoformat(input_data['begin_date'])
    assert booking.end_date == datetime.date.fromisoformat(input_data['end_date'])
    assert booking.room_id == input_data['room_id']


@pytest.mark.parametrize('field', ['begin_date', 'end_date', 'room_id'])
@pytest.mark.django_db
def test_booking_create_without_required_field(client, room_input, booking_input, field):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    del input_data[field]
    response = client.post(reverse('booking-list'), data=input_data)

    assert response.status_code == 400


@pytest.mark.parametrize('begin_date', ['', '2021-01-0', '2021-02-30'])
@pytest.mark.django_db
def test_booking_create_invalid_begin_date(client, room_input, booking_input, begin_date):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    response = client.post(reverse('booking-list'), data={**input_data, 'begin_date': begin_date})

    assert response.status_code == 400


@pytest.mark.parametrize('end_date', ['', '2021-01-0', '2021-02-30'])
@pytest.mark.django_db
def test_booking_create_invalid_end_date(client, room_input, booking_input, end_date):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    response = client.post(reverse('booking-list'), data={**input_data, 'end_date': end_date})

    assert response.status_code == 400


@pytest.mark.parametrize('room_id', ['', 'N'])
@pytest.mark.django_db
def test_booking_create_invalid_room_id(client, booking_input, room_id):
    response = client.post(reverse('booking-list'), data={**booking_input, 'room_id': room_id})

    assert response.status_code == 400


@pytest.mark.django_db
def test_booking_create_end_date_preceds_begin_date(client, room_input):
    room = Room.objects.create(**room_input)
    response = client.post(reverse('booking-list'), data={
        'begin_date': '2021-01-07',
        'end_date': '2021-01-01',
        'room_id': room.id
    })

    assert response.status_code == 400


@pytest.mark.parametrize('dates', [
    # inside of the date range
    {'begin_date': '2021-01-07', 'end_date': '2021-01-13'},
    {'begin_date': '2021-01-06', 'end_date': '2021-01-14'},
    {'begin_date': '2021-01-07', 'end_date': '2021-01-14'},
    # outside of the date range
    {'begin_date': '2021-01-06', 'end_date': '2021-01-15'},
    {'begin_date': '2021-01-06', 'end_date': '2021-01-14'},
    {'begin_date': '2021-01-07', 'end_date': '2021-01-15'},
    # crosses the left border
    {'begin_date': '2021-01-06', 'end_date': '2021-01-13'},
    {'begin_date': '2021-01-06', 'end_date': '2021-01-07'},
    # crosses the right border
    {'begin_date': '2021-01-13', 'end_date': '2021-01-15'},
    {'begin_date': '2021-01-14', 'end_date': '2021-01-15'},
])
@pytest.mark.django_db
def test_booking_create_overlapping_dates(client, room_input, dates):
    room = Room.objects.create(**room_input)

    booking_1 = {
        'begin_date': '2021-01-07',
        'end_date': '2021-01-14',
        'room_id': room.id
    }
    Booking.objects.create(**booking_1)

    booking_2 = {
        **dates,
        'room_id': room.id
    }
    response = client.post(reverse('booking-list'), data=booking_2)

    assert response.status_code == 400
