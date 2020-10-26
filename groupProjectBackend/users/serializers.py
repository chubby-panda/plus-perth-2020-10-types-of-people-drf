from rest_framework import serializers
# from allauth.account.util import setup_user_email
# from rest_auth.registration.serializers import RegisterSerializer
from .models import CustomUser, OrgProfile, MentorProfile

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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, data):
        if not data.get('password') or not data.get('password2'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class MentorProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField(source='user.usermame')
    user = serializers.ReadOnlyField(source='user.username')
    bio = serializers.CharField(max_length=5000)
    name = serializers.CharField(max_length=300)
    
    class Meta:
        model = MentorProfile
        fields = ['id', 'name', 'user', 'username','bio']
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