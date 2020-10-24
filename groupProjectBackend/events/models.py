from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    category = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category

class Event(models.Model):
    event_name = models.CharField(max_length=120)
    event_description = models.TextField(max_length=500)
    event_image = models.URLField(max_length=120)
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=120)
    # organiser = models.CharField(max_length=26)
    organiser = models.ForeignKey(
                get_user_model(),
                on_delete=models.CASCADE,
                related_name='organiser_events'
    )
    category = models.ForeignKey(
               Category,
               on_delete=models.CASCADE,
               related_name='event_categories'
    )



