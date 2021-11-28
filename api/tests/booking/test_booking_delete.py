import datetime

import pytest

from rest_framework.reverse import reverse

from api.models import Booking, Room


@pytest.mark.django_db
def test_delete_booking_success(client, room_input, booking_input):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    booking = Booking.objects.create(**input_data)
    booking_id = booking.id

    response = client.delete(reverse('booking-detail', args=[booking_id]))

    assert response.status_code == 204

    assert not Booking.objects.filter(pk=booking_id).exists()


@pytest.mark.django_db
def test_delete_room_not_found(client, room_input, booking_input):
    room = Room.objects.create(**room_input)
    input_data = {**booking_input, 'room_id': room.id}
    booking = Booking.objects.create(**input_data)
    booking_id = booking.id

    response = client.delete(reverse('booking-detail', args=[booking_id + 1]))

    assert response.status_code == 404
