from rest_framework import serializers
# from allauth.account.util import setup_user_email
# from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser, OrgProfile, MentorProfile
from events.models import Category


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'is_org',)

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MentorProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='user.usermame')
    user = serializers.ReadOnlyField(source='user.username')
    mentor_image = serializers.URLField(default = "https://cdn.pixabay.com/photo/2015/03/03/08/55/portrait-657116_960_720.jpg")
    bio = serializers.CharField(max_length=5000)
    name = serializers.CharField(max_length=300)
    location = serializers.CharField(max_length=300)
    latitude = serializers.DecimalField(
        max_digits=15, decimal_places=10, default=-31.95351)
    longitude = serializers.DecimalField(
        max_digits=15, decimal_places=10, default=115.85705)
    skills = serializers.SlugRelatedField(
        many=True, slug_field="category", queryset=Category.objects.all())

    class Meta:
        model = MentorProfile
        fields = ['id', 'name', 'user', 'username', 'bio',
                  'mentor_image', 'skills', 'location', 'latitude', 'longitude', ]
        lookup_field = 'username'

    def create(self, validated_data):
        return MentorProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        skills_updated = False
        # Get the skills from the input data
        if validated_data.get('skills', None) is not None:
            skills_data = validated_data.pop('skills')
            # Get the current skills
            skills = instance.skills
            skills_updated = True

        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.mentor_image = validated_data.get('mentor_image', instance.mentor_image)
        instance.location = validated_data.get('location', instance.location)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get(
            'longitude', instance.longitude)
        instance.save()

        # Reset the skills data
        if skills_updated:
            skills.clear()
            skills.set(skills_data)

        instance.save()
        return instance


class OrgProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    company_name = serializers.CharField(max_length=300)
    contact_name = serializers.CharField(max_length=300)
    org_image = serializers.URLField(default = "https://cdn.pixabay.com/photo/2015/03/03/08/55/portrait-657116_960_720.jpg")
    org_bio = serializers.CharField(max_length=5000)
    username = serializers.ReadOnlyField(source='user.usermame')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = OrgProfile
        fields = ['id', 'company_name', 'contact_name',
                  'user', 'username', 'org_bio', 'org_image']
        lookup_field = 'username'

    def create(self, validated_data):
        return OrgProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get(
            'company_name', instance.company_name)
        instance.org_image = validated_data.get('org_image', instance.org_image)
        instance.org_bio = validated_data.get('org_bio', instance.org_bio)
        instance.contact_name = validated_data.get(
            'contact_name', instance.contact_name)
        instance.save()
        return instance
