from django.shortcuts import render
from django.http import Http404
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Category, Register
from users.models import CustomUser
from .serializers import EventSerializer, EventDetailSerializer, CategoryProjectSerializer, CategorySerializer, RegisterSerializer, MentorCategory
from .permissions import IsOwnerOrReadOnly, isSuperUser, IsOrganisationOrReadOnly


class CategoryList(APIView):
    """
    Returns list of all categories
    """
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


class CategoryDetail(APIView):
    """
    Returns details of specified category
    """
    permission_classes = [isSuperUser, ]
    serializer_class = CategorySerializer

    def get_object(self, category):
        try:
            return Category.objects.get(category=category)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category):
        category_object = self.get_object(category)
        serializer = CategorySerializer(category_object)
        return Response(serializer.data)

    def put(self, request, category):
        category_object = self.get_object(category)
        self.check_object_permissions(request, category_object)
        data = request.data
        serializer = CategorySerializer(
            instance=category_object,
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

    def delete(self, request, category):
        category_object = self.get_object(category)
        self.check_object_permissions(request, category_object)

        try:
            category_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            raise Http404


class EventList(APIView):
    """
    Returns list of all open events
    """
    permission_classes = [IsOrganisationOrReadOnly]

    def get(self, request):
        events = Event.objects.filter(is_open=True)
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


class CategoryProjectList(APIView):
    """
    Returns list of projects of specified category
    """

    def get(self, request, category):
        events = Event.objects.filter(categories__category=category)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetail(APIView):
    """
    Returns details of specified event
    """
    permission_classes = [IsOwnerOrReadOnly]
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


class MentorsRegisterList(APIView):
    """
    Returns a list of mentors for specified event
    Posts a mentor register object
    """

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        responses = Register.objects.all().filter(event=self.get_object(pk))
        serializer = RegisterSerializer(responses, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(event=self.get_object(pk), mentor=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MentorAttendanceView(APIView):

    def get_object(self, username):
        try:
            return CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, username):
        mentor = self.get_object(username=username)
        attended = Register.objects.all().filter(mentor=mentor)
        serializer = MentorCategory(attended, many=True)
        return Response(serializer.data)

class EventHostedView(APIView):

    def get(self, request, username):
        organiser = CustomUser.objects.get(username=username)
        hosted = Event.objects.all().filter(organiser=organiser)
        serializer = EventSerializer(hosted, many=True)
        return Response(serializer.data)