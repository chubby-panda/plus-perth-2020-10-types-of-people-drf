from rest_framework import serializers
from .models import Event, Category, Register


class CategorySerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    category = serializers.CharField(max_length=100)
    category_icon = serializers.URLField(
        max_length=120, default="https://via.placeholder.com/300.jpg")
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
    event_date = serializers.DateTimeField()
    event_location = serializers.CharField(max_length=120)
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
    event_id = serializers.IntegerField()
    mentor = serializers.ReadOnlyField(source='mentor.username')

    def create(self, validated_data):
        return Register.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.mentor = validated_data.get('mentor', instance.mentor)
        instance.event_id = validated_data.get('event_id', instance.event_id)
        instance.save()
        return instance


class EventDetailSerializer(EventSerializer):
    responses = RegisterSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
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
        instance.event_date = validated_data.get(
            'event_date', instance.event_date)
        instance.event_location = validated_data.get(
            'event_location', instance.event_location)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class MentorCategory(serializers.Serializer):
    event_id = serializers.IntegerField()
    mentor = serializers.ReadOnlyField(source='mentor.username')
