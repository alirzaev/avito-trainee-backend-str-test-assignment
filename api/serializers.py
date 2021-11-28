from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=5, max_length=200)

    price = serializers.DecimalField(min_value=1.00, max_digits=9, decimal_places=2)

    class Meta:
        model = Room
        
        fields = ('id', 'description', 'price', 'created_at',)


class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source='room', queryset=Room.objects.all())

    class Meta:
        model = Booking

        fields = ('id', 'begin_date', 'end_date', 'room_id',)
    
    def validate(self, data):
        if data['begin_date'] > data['end_date']:
            raise serializers.ValidationError('begin_date must be less than or equal to end_date')
        
        return data
