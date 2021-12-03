from django.db.models.query_utils import Q
from django_filters import rest_framework as django_filters
from drf_spectacular import types
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters, mixins, serializers, viewsets

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


@extend_schema_view(
    list=extend_schema(
        summary='Get a list of rooms',
        tags=['room'],
        auth=[{}],
        examples=[
            OpenApiExample(
                name='A valid output example',
                value=[
                    {
                        'id': 1,
                        'description': 'Double room',
                        'price': '100',
                        'created_at': '2021-01-01'
                    }
                ],
                response_only=True,
            )
        ]
    ),
    create=extend_schema(
        summary='Add a new room',
        tags=['room'],
        auth=[{}],
        examples=[
            OpenApiExample(
                name='A valid input example',
                value={
                    'description': 'Double room',
                    'price': '100'
                },
                request_only=True
            ),
            OpenApiExample(
                name='A valid output example',
                value={
                    'id': 1,
                    'description': 'Double room',
                    'price': '100',
                    'created_at': '2021-01-01'
                },
                response_only=True,
            )
        ]
    ),
    destroy=extend_schema(
        summary='Delete a room and all related bookings',
        tags=['room'],
        auth=[{}]
    )
)
class RoomView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Room.objects.all()

    serializer_class = RoomSerializer

    filter_backends = (filters.OrderingFilter,)

    ordering_fields = ('created_at', 'price',)


@extend_schema_view(
    list=extend_schema(
        summary='Get a booking list of the specified room',
        tags=['booking'],
        auth=[{}],
        parameters=[
            OpenApiParameter(
                name='room',
                description='A unique integer value identifying the room.',
                type=types.OpenApiTypes.INT
            )
        ],
        examples=[
            OpenApiExample(
                name='A valid output example',
                value=[
                    {
                        'id': 1,
                        'begin_date': '2021-01-01',
                        'end_date': '2021-01-07',
                        'room_id': 1
                    }
                ],
                response_only=True,
            )
        ]
    ),
    create=extend_schema(
        summary='Add a new booking',
        tags=['booking'],
        auth=[{}],
        examples=[
            OpenApiExample(
                name='A valid input example',
                value={
                    'begin_date': '2021-01-01',
                    'end_date': '2021-01-07',
                    'room_id': 1
                },
                request_only=True
            ),
            OpenApiExample(
                name='A valid output example',
                value={
                    'id': 1,
                    'begin_date': '2021-01-01',
                    'end_date': '2021-01-07',
                    'room_id': 1
                },
                response_only=True,
            )
        ]
    ),
    destroy=extend_schema(
        summary='Delete a booking',
        tags=['booking'],
        auth=[{}]
    )
)
class BookingView(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Booking.objects.all()

    serializer_class = BookingSerializer

    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)

    filterset_fields = ('room',)

    ordering_fields = ('begin_date',)

    def perform_create(self, serializer):
        begin_date = serializer.validated_data['begin_date']
        end_date = serializer.validated_data['end_date']
        room = serializer.validated_data['room']

        ok = Booking.objects.filter(
            ~Q(Q(begin_date__gt=end_date) | Q(end_date__lt=begin_date)) &
            Q(room=room)
        ).count() == 0
        if ok:
            return super().perform_create(serializer)
        
        raise serializers.ValidationError({
            'non_field_errors': ['OVERLAPPING_DATES']
        })
