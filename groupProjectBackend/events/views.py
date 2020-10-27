from django.shortcuts import render
from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Category, Register
from .serializers import EventSerializer, EventDetailSerializer, CategoryProjectSerializer, CategorySerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly, isSuperUser


class CategoryList(APIView):
    permission_classes = [isSuperUser, permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            # print(request.user.is_superuser)
            if (request.user.is_superuser):
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


class EventList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organiser=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        print(serializer)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryProject(generics.RetrieveAPIView):
    permission_classes = [isSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategoryProjectSerializer
    lookup_field = 'category'


class EventDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = EventDetailSerializer

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        self.check_object_permissions(request, event)
        data = request.data
        serializer = EventDetailSerializer(
            instance=event,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        event = self.get_object(pk)
        self.check_object_permissions(request, event)

        try:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            raise Http404


# class Mentors_Register_List(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def get(self, request):
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)

class MentorsRegisterList(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        registers = Register.objects.all()
        serializer = RegisterSerializer(registers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(mentor=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
