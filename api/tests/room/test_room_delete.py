import datetime

import pytest

from rest_framework.reverse import reverse

from api.models import Booking, Room


@pytest.mark.django_db
def test_delete_room_success(client, room_input):
    room = Room.objects.create(**room_input)
    room_id = room.id

    response = client.delete(reverse('room-detail', args=[room_id]))

    assert response.status_code == 204

    assert not Room.objects.filter(pk=room_id).exists()


@pytest.mark.django_db
def test_delete_room_not_found(client, room_input):
    room = Room.objects.create(**room_input)
    room_id = room.id + 1

    response = client.delete(reverse('room-detail', args=[room_id]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_room_with_booking(client, room_input):
    room = Room.objects.create(**room_input)
    room_id = room.id
    Booking.objects.create(
        room=room,
        begin_date=datetime.date(2021, 1, 1),
        end_date=datetime.date(2021, 1, 7)
    )

    response = client.delete(reverse('room-detail', args=[room_id]))

    assert response.status_code == 204

    bookings_count = Booking.objects.filter(room__id=room_id).count()

    assert bookings_count == 0
