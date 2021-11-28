import pytest

from rest_framework.reverse import reverse

from api.models import Room


@pytest.mark.django_db
def test_room_create_success(client, room_input):
    response = client.post(reverse('room-list'), data=room_input)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data

    room = Room.objects.get(pk=data['id'])
    assert room.description == room_input['description']
    assert room.price == room_input['price']


@pytest.mark.parametrize('field', ['description', 'price'])
@pytest.mark.django_db
def test_room_create_without_required_field(client, room_input, field):
    input_data = {**room_input}
    del input_data[field]
    response = client.post(reverse('room-list'), data=input_data)

    assert response.status_code == 400


@pytest.mark.parametrize('description', ['', 'N' * 4, 'N' * 201])
@pytest.mark.django_db
def test_room_create_invalid_description(client, room_input, description):
    response = client.post(reverse('room-list'), data={**room_input, 'description': description})

    assert response.status_code == 400


@pytest.mark.parametrize('price', [0, 0.99, 10_000_000.00])
@pytest.mark.django_db
def test_room_create_invalid_price(client, room_input, price):
    response = client.post(reverse('room-list'), data={**room_input, 'price': price})

    assert response.status_code == 400