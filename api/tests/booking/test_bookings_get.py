import pytest

from rest_framework.reverse import reverse

from api.models import Booking, Room


@pytest.fixture
def bookings_inputs():
    return [
        [
            {
                'begin_date': '2021-01-01',
                'end_date': '2021-01-07',
                'room_id': 1
            },
            {
                'begin_date': '2021-01-08',
                'end_date': '2021-01-14',
                'room_id': 1
            }
        ],
        [
            {
                'begin_date': '2021-02-01',
                'end_date': '2021-02-07',
                'room_id': 2
            },
            {
                'begin_date': '2021-02-08',
                'end_date': '2021-02-14',
                'room_id': 2
            }
        ]
    ]


@pytest.fixture
def rooms_input():
    return [
        {
            'description': 'Room #1',
            'price': 100
        },
        {
            'description': 'Room #2',
            'price': 100
        }
    ]


@pytest.mark.django_db
def test_get_bookings_several_rooms_success(client, rooms_input, bookings_inputs):
    assert len(rooms_input) == len(bookings_inputs)

    rooms = [Room.objects.create(**data) for data in rooms_input]

    bookings = [
        [
            Booking.objects.create(**{**data, 'room_id': room.id})
            for data in bookings_input
        ] for room, bookings_input in zip(rooms, bookings_inputs)
    ]

    for room, bookings in zip(rooms, bookings):
        response = client.get(reverse('booking-list'), data={
            'room': room.id,
            'ordering': 'begin_date'
        })

        assert response.status_code == 200

        actual = [booking['id'] for booking in response.json()]
        expected = [
            booking.id for booking in sorted(bookings, key=lambda b: b.begin_date)
        ]

        assert actual == expected


@pytest.mark.django_db
def test_get_bookings_room_not_found(client, room_input):
    room = Room.objects.create(**room_input)

    response = client.get(reverse('booking-list'), data={
        'room': room.id + 1,
        'ordering': 'begin_date'
    })

    assert response.status_code == 400
