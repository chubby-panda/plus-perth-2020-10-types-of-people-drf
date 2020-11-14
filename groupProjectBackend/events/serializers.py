from users.models import MentorProfile
from django.db.models.fields import DateTimeField
from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Event, Category, Register


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    category = serializers.CharField(max_length=100)
    # category_icon = serializers.URLField(
    #     max_length=120, default="https://via.placeholder.com/300.jpg")
    lookup_field = 'category'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class EventSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    event_name = serializers.CharField(max_length=120)
    event_description = serializers.CharField(max_length=500)
    event_image = serializers.URLField(max_length=120)
    is_open = serializers.BooleanField(default=True)
    date_created = serializers.DateTimeField(read_only=True)
    event_datetime_start = serializers.DateTimeField()
    event_datetime_end = serializers.DateTimeField()
    event_location = serializers.CharField(
        max_length=300,  default="Perth, WA, Australia")
    latitude = serializers.DecimalField(
        max_digits=15, decimal_places=10, default=-31.95351)
    longitude = serializers.DecimalField(
        max_digits=15, decimal_places=10, default=115.85705)
    organiser = serializers.ReadOnlyField(source='organiser.username')
    categories = serializers.SlugRelatedField(
        many=True, slug_field="category", queryset=Category.objects.all())

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        event = Event.objects.create(**validated_data)
        event.categories.set(categories)
        event.save()
        return event


class CategoryProjectSerializer(CategorySerializer):
    event_categories = EventSerializer(many=True, read_only=True)


class RegisterSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    event = serializers.ReadOnlyField(source='event.id')
    mentor = serializers.ReadOnlyField(source='mentor.username')
    date_registered = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Register.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.mentor = validated_data.get('mentor', instance.mentor)
        instance.event_id = validated_data.get('event_id', instance.event_id)
        instance.save()
        return instance


class AttendanceSerializer(serializers.Serializer):
    """added to allow orgs to mark attendance"""
    id = serializers.ReadOnlyField()
    event = serializers.ReadOnlyField(source='event.id')
    mentor = serializers.ReadOnlyField(source='mentor.username')
    attended = serializers.BooleanField()

    def update(self, instance, validated_data):
        instance.attended = validated_data.get('attended', instance.attended)
        instance.save()
        return instance


class EventDetailSerializer(EventSerializer):
    responses = RegisterSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):

        categories_updated = False
        # Get the categories from the input data
        if validated_data.get('categories', None) is not None:
            categories_data = validated_data.pop('categories')
            # Get the current categories
            categories = instance.categories
            categories_updated = True

        # Update the other fields
        instance.event_name = validated_data.get(
            'event_name', instance.event_name)
        instance.event_description = validated_data.get(
            'event_description', instance.event_description)
        instance.event_image = validated_data.get(
            'event_image', instance.event_image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get(
            'date_created', instance.date_created)
        instance.organiser = validated_data.get(
            'organiser', instance.organiser)
        instance.event_datetime_start = validated_data.get(
            'event_datetime_start', instance.event_datetime_start)
        instance.event_datetime_end = validated_data.get(
            'event_datetime_end', instance.event_datetime_end)
        instance.event_location = validated_data.get(
            'event_location', instance.event_location)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get(
            'longitude', instance.longitude)
        instance.save()

        # Reset the categories data
        if categories_updated:
            categories.clear()
            categories.set(categories_data)

        instance.save()
        return instance


class MentorCategory(serializers.Serializer):
    event_id = serializers.IntegerField()
    mentor = serializers.ReadOnlyField(source='mentor.username')


class MentorEventAttendanceSerializer(serializers.Serializer):
    """serializer to return mentors who responded to one event"""
    id = serializers.ReadOnlyField()
    event = serializers.ReadOnlyField(source='event.id')
    mentor = serializers.ReadOnlyField(source='mentor.username')
    attended = serializers.BooleanField(source='register.pk')


class RegisterMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['mentor', 'attended']


class BulkAttendanceUpdateSerializer(serializers.ModelSerializer):
    """
    This allows for bulk update of mentors who attended the event

    """
    responses = RegisterMentorSerializer(many=True)

    class Meta:
        model = Event
        fields = ['responses']
