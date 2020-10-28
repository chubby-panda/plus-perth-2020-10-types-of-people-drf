from rest_framework import serializers
# from allauth.account.util import setup_user_email
# from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser, OrgProfile, MentorProfile
from events.models import Category

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password','is_org',)


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
    bio = serializers.CharField(max_length=5000)
    name = serializers.CharField(max_length=300)
    
    class Meta:
        model = MentorProfile
        fields = ['id', 'name', 'user', 'username','bio', 'skills']
        lookup_field = 'username'

    def create(self, validated_data):
        return MentorProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance


class OrgProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    company_name = serializers.CharField(max_length=300)
    contact_name = serializers.CharField(max_length=300)
    org_bio = serializers.CharField(max_length=5000)
    username = serializers.ReadOnlyField(source='user.usermame')
    user = serializers.ReadOnlyField(source='user.username')

    
    class Meta:
        model = OrgProfile
        fields = ['id', 'company_name', 'contact_name', 'user', 'username','org_bio']
        lookup_field = 'username'

    def create(self, validated_data):
        return OrgProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.org_bio = validated_data.get('org_bio', instance.org_bio)
        instance.contact_name = validated_data.get('contact_name', instance.contact_name)
        instance.save()
        return instance