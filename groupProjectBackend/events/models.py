from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)
    category_icon = models.URLField(
        max_length=120, default="https://via.placeholder.com/300.jpg")

    def __str__(self):
        return self.category


class Event(models.Model):
    event_name = models.CharField(max_length=120)
    event_description = models.TextField(max_length=500)
    event_image = models.URLField(max_length=120)
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    event_date = models.DateTimeField()
    event_location = models.CharField(max_length=120)
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
    # mentor_event_response_id =
    # what is the mentor event response id
    # prefer mentor username over mentor_id?
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
    # attended to be a later feature?
    # attended = models.BooleanField(default=True)

# class MentorCategory(models.Model):
#     # mentor_id or username??
#     mentor_category_id =
#     mentor = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         related_name='mentor_response'
#     )


# class EventCategory(models.Model):
#     mevent_category_id =
#     event_id =
#     category_id =
