from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from .models import CustomUser, MentorProfile, OrgProfile
from .serializers import CustomUserSerializer, MentorProfileSerializer, OrgProfileSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .permissions import IsOwnerOrReadOnly


class CustomUserCreate(generics.CreateAPIView):
    """
    View for registering new account.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    def check_permissions(self, request):
        if request.user.is_authenticated:
            self.permission_denied(request)

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class CustomUserDetail(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    lookup_field = 'username'

    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username):
        user = self.get_object(username)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, 
                status = status.HTTP_200_OK
            )
        return Response (
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, username):
        user = self.get_object(username)
        self.check_object_permissions(request, user)

        try:
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            raise Http404

class MentorProfile(APIView):
    permission_classes = IsOwnerOrReadOnly

    def get_object(self, username):
        try:
            mentor_profile = MentorProfile.objects.select_related('user').get(user__username=username)
            self.check_object_permissions(self.request, mentor_profile)
            return mentor_profile
        except MentorProfile.DoesNotExist():
            raise Http404
    
    def get(self, request, username):
        mentor_profile = self.get_object(username)
        serializer= MentorProfileSerializer(mentor_profile)
        return Response(serializer.data)

    def put(self, request, username):
        mentor_profile = self.get_object(username)
        serializer = MentorProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
        return Response(
            serializer.data,
            status.HTTP_400_BAD_REQUEST
        )

class OrgProfile(APIView):
    permission_classes = IsOwnerOrReadOnly

    def get_object(self, username):
        try:
            org_profile = OrgProfile.objects.select_related('user').get(user__username=username)
            self.check_object_permissions(self.request, org_profile)
            return org_profile
        except OrgProfile.DoesNotExist():
            raise Http404
    
    def get(self, request, username):
        org_profile = self.get_object(username)
        serializer= OrgProfileSerializer(org_profile)
        return Response(serializer.data)

    def put(self, request, username):
        org_profile = self.get_object(username)
        serializer = OrgProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
        return Response(
            serializer.data,
            status.HTTP_400_BAD_REQUEST
        )