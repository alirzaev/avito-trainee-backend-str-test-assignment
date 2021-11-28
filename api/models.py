from django.db import models
from django.db.models.fields.related import ForeignKey


class Room(models.Model):
    description = models.CharField(max_length=200)

    price = models.DecimalField(decimal_places=2, max_digits=9, db_index=True)

    created_at = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.description}'


class Booking(models.Model):
    begin_date = models.DateField(db_index=True)

    end_date = models.DateField()

    room = ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking of '{self.room} ({self.begin_date}-{self.end_date})"
