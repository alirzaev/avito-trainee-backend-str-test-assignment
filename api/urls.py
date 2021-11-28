from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookingView, RoomView

router = DefaultRouter()
router.register('booking', BookingView)
router.register('room', RoomView)

urlpatterns = router.urls
