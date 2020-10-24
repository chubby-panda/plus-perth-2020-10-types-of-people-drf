from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied 

class CustomUserList(APIView):

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

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
                status = status.HTTP_201_CREATED
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