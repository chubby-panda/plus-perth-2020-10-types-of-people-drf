from rest_framework import serializers
from .models import Event, Category

class CategorySerializer(serializers.Serializer):
    category = serializers.CharField(max_length=100)
    lookup_field = 'category'
        
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class EventSerializer(serializers.Serializer):
    event_id = serializers.ReadOnlyField()
    event_name = serializers.CharField(max_length=120)
    event_description = serializers.CharField(max_length=500)
    event_image = serializers.URLField(max_length=120)
    is_open = serializers.BooleanField()
    date_created = serializers.DateTimeField()
    event_date = serializers.DateTimeField()
    event_location = serializers.CharField(max_length=120)
    # organiser = serializers.CharField(max_length=26)
    organiser = serializers.ReadOnlyField(source='organiser.username')
    category = serializers.SlugRelatedField(queryset = Category.objects.all(), read_only = False, slug_field='category')


    def create(self, validated_data):
        return Event.objects.create(**validated_data)

class CategoryProjectSerializer(CategorySerializer):
    event_categories = EventSerializer(many=True, read_only=True)


class EventDetailSerializer(EventSerializer):
    def update(self, instance, validated_data):
        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.event_description = validated_data.get('event_description', instance.event_description)
        instance.event_image = validated_data.get('event_image', instance.event_image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.organiser = validated_data.get('organiser', instance.organiser)
        instance.event_date = validated_data.get('event_date', instance.event_date)
        instance.event_location = validated_data.get('event_location', instance.event_location)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance