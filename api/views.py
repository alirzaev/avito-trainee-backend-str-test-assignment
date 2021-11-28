from django.db.models.query_utils import Q
from django_filters import rest_framework as django_filters
from rest_framework import filters, mixins, serializers, viewsets

from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


class RoomView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Room.objects.all()

    serializer_class = RoomSerializer

    filter_backends = (filters.OrderingFilter,)

    ordering_fields = ('created_at', 'price',)


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
