import datetime

import pytest

from rest_framework.reverse import reverse

from api.models import Room


@pytest.fixture
def rooms_input():
    return [{
        'description': f'Room #{i}',
        'price': price
    } for i, price in enumerate((200, 100, 100, 150), 1)] # 1..4


@pytest.mark.django_db
def test_get_rooms_empty_response(client):
    response = client.get(reverse('room-list'))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_get_rooms_price_asc(client, rooms_input):
    for data in rooms_input:
        Room.objects.create(**data)

    response = client.get(reverse('room-list'), data={
        'ordering': 'price'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('price')
    ]

    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_price_desc(client, rooms_input):
    for data in rooms_input:
        Room.objects.create(**data)

    response = client.get(reverse('room-list'), data={
        'ordering': '-price'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('-price')
    ]

    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_date_asc(client, rooms_input):
    rooms = [Room.objects.create(**data) for data in rooms_input]

    for i, room in enumerate(rooms, 1):
        room.created_at = datetime.date(2021, 1, i)
        room.save()

    response = client.get(reverse('room-list'), data={
        'ordering': 'created_at'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('created_at')
    ]

    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_date_desc(client, rooms_input):
    rooms = [Room.objects.create(**data) for data in rooms_input]

    for i, room in enumerate(rooms, 1):
        room.created_at = datetime.date(2021, 1, i)
        room.save()

    response = client.get(reverse('room-list'), data={
        'ordering': '-created_at'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('-created_at')
    ]

    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_price_asc_date_asc(client, rooms_input):
    rooms = [Room.objects.create(**data) for data in rooms_input]

    for i, room in enumerate(rooms, 1):
        room.created_at = datetime.date(2021, 1, i)
        room.save()

    response = client.get(reverse('room-list'), data={
        'ordering': 'price,created_at'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('price', 'created_at')
    ]

    assert actual == expected


@pytest.mark.django_db
def test_get_rooms_price_desc_date_desc(client, rooms_input):
    rooms = [Room.objects.create(**data) for data in rooms_input]

    for i, room in enumerate(rooms, 1):
        room.created_at = datetime.date(2021, 1, i)
        room.save()

    response = client.get(reverse('room-list'), data={
        'ordering': '-price,-created_at'
    })

    assert response.status_code == 200

    actual = [room['id'] for room in response.json()]
    expected = [
        room.id for room in Room.objects.order_by('-price', '-created_at')
    ]

    assert actual == expected
