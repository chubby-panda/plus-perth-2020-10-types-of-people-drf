from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    # category_icon = models.URLField(
    #     max_length=120, default="https://via.placeholder.com/300.jpg")
    # category icon removed from backend for now

    def __str__(self):
        return self.category


class Event(models.Model):
    event_name = models.CharField(max_length=120)
    event_description = models.TextField(max_length=500)
    event_image = models.URLField(max_length=120)
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    event_datetime_start = models.DateTimeField()
    event_datetime_end = models.DateTimeField()
    event_location = models.CharField(max_length=300, default="Perth, WA, Australia")
    latitude = models.DecimalField(
        max_digits=15, decimal_places=10, default=-31.95351)
    longitude = models.DecimalField(
        max_digits=15, decimal_places=10, default=115.85705)
    organiser = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='organiser_events'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='events',
        related_query_name='event'
    )


class Register(models.Model):
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='responses'
    )
    mentor = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='mentor_response'
    )
    date_registered = models.DateTimeField(auto_now_add=True, editable=False)
    attended = models.BooleanField(default=False)
