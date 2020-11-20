from django.core.exceptions import RequestDataTooBig
from django.shortcuts import render
from django.db.models import Count, Q
from django.http import Http404
from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from .models import Event, Category, Register, EventImage
from .serializers import BulkAttendanceUpdateSerializer, EventSerializer, EventDetailSerializer, CategoryProjectSerializer, CategorySerializer, MentorEventAttendanceSerializer, RegisterSerializer, MentorCategory, EventImageSerializer
from .permissions import IsOwnerOrReadOnly, IsSuperUser, IsOrganisationOrReadOnly, HasNotRegistered, IsOrganiserOrReadOnly
from users.models import CustomUser, MentorProfile
from math import radians, cos, sin, asin, sqrt
from itertools import chain
from django.db.models import F, Func
from django.db.models.functions import Sin, Cos, Sqrt, ASin, Radians, ATan2


class CategoryList(APIView):
    """
    Returns list of all categories
    """
    permission_classes = [IsSuperUser, ]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.check_permissions(request)
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
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
    permission_classes = [IsSuperUser, ]
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
        events = Event.objects.filter(is_open=True)[:30]
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


class EventSearchView(generics.ListAPIView):
    """
    Filters all events using search parameters
    """
    serializer_class = EventSerializer

    def get_queryset(self):
        query = self.request.query_params['query']
        queryset = Event.objects.filter(Q(event_name__icontains=query) | Q(event_description__icontains=query) | Q(event_location__icontains=query) | Q(
            categories__category__icontains=query) | Q(organiser__username__icontains=query) | Q(organiser__org_profile__company_name__icontains=query)).order_by('-date_created').distinct()[:30]
        return queryset


class PopularEventsList(APIView):
    """
    Returns list of projects from most responses to least
    """

    def get(self, request):
        events = Event.objects.annotate(num_responses=Count(
            'responses')).order_by('-num_responses')[:30]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class PopularEventsShortList(APIView):
    """
Returns shortlist (6) of projects from most responses to least
    """

    def get(self, request):
        events = Event.objects.annotate(num_responses=Count(
            'responses')).order_by('-num_responses')[:6]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class LocationEventsList(APIView):
    """
    Returns list of events within a specifed distance of a logged-in user (closest to furthest)
    Pass the kms into the url
    """

    def get(self, request, kms):
        # Get user coordinates
        profile = MentorProfile.objects.get(user=request.user)
        latitude = float(profile.latitude)
        longitude = float(profile.longitude)
        radius = 6378.137  # this is in kms

        # Filter events by distance from user location using Great Circle formula
        events = Event.objects.annotate(distance=(
            radius * (2 * ATan2(Sqrt(Sin((Radians(F('latitude')) - Radians(latitude))/2) ** 2 + Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) * Sin((Radians(F('longitude')) - Radians(longitude))/2)**2),
                                Sqrt(1 - (Sin((Radians(F('latitude')) - Radians(latitude))/2) ** 2 + Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) * Sin((Radians(F('longitude')) - Radians(longitude))/2)**2))))
        )).filter(distance__lte=kms).order_by('distance')[:30]

        for event in events:
            print("EVENT DISTANCE", event.distance)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class CategoryProjectList(APIView):
    """
    Returns list of projects of specified category
    """

    def get(self, request, category):
        events = Event.objects.filter(categories__category=category)[:30]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class CategoryProjectShortList(APIView):
    """
    Returns shortlist (6) of projects of specified category
    """

    def get(self, request, category):
        events = Event.objects.filter(categories__category=category)[:6]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetail(APIView):
    """
    Returns details of specified event
    """
    permission_classes = [IsOwnerOrReadOnly, ]
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


class EventImageList(APIView):
    """
    A view for uploading and retrieving event images
    """
    queryset = EventImage.objects.all()
    serializer_class = EventImageSerializer
    parser_classes = (FileUploadParser,)

    def get_object(self, pk):
        try:
            event = Event.objects.get(pk=pk)
            self.check_object_permissions(self.request, event)
            return event
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        images = EventImage.objects.all().filter(event=self.get_object(pk))
        serializer = EventImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = EventImageSerializer(data={'image': request.data['file']})
        if serializer.is_valid():
            serializer.save(event=self.get_object(pk))
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EventImageDetail(APIView):
    """
    A view for updating, deleting and retrieving a single event image
    """
    parser_classes = (FileUploadParser,)
    serializer_class = EventImageSerializer

    def get_object(self, image_pk):
        try:
            image = EventImage.objects.get(pk=image_pk)
            self.check_object_permissions(self.request, image)
            return image
        except EventImage.DoesNotExist:
            raise Http404

    def get(self, request, event_pk, image_pk):
        image = self.get_object(image_pk)
        serializer = EventImageSerializer(image)
        return Response(serializer.data)

    def put(self, request, event_pk, image_pk):
        image = self.get_object(image_pk)
        serializer = EventImageSerializer(
            image, data={'image': request.data['file']})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, event_pk, image_pk):
        image = self.get_object(image_pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MentorsRegisterList(APIView):
    """
    Returns a list of mentors for specified event
    Posts a mentor register object
    """
    permission_classes = [HasNotRegistered, ]

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
        self.check_object_permissions(request, pk)
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

    def delete(self, request, pk):
        event_registrations = Register.objects.all().filter(event=self.get_object(pk))
        user_registration = event_registrations.filter(mentor=request.user)
        if len(user_registration) > 0:
            user_registration.delete()
            return Response(
                status=status.HTTP_200_OK
            )
        if len(user_registration) == 0:
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )


class MentorsRegisterDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = RegisterSerializer


class MentorAttendanceView(APIView):
    """
    Returns a list of all mentors who have expressed interest in an event.
    The attended variable here just refers to whether or not they expressed interest, 
    not whether they actually attended the event.
    """

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
    """
    This returns a list of all events (open and closed) by an organiser
    """

    def get(self, request, username):
        organiser = CustomUser.objects.get(username=username)
        hosted = Event.objects.all().filter(organiser=organiser)
        serializer = EventSerializer(hosted, many=True)

        return Response(serializer.data)


class EventAttendenceView(APIView):
    """
    Returns a view of all mentors registered for an event.
    Allows orgs to mark if mentors attended their event
    Allows for Bulk Update - But Permissions not working correctly.
    """
    # permission_classes = [IsOrganiserOrReadOnly, ]
    serializer = BulkAttendanceUpdateSerializer

    def get(self, request, pk):
        serializer = self.serializer(instance=Event.objects.get(pk=pk))
        return Response(serializer.data)

    def put(self, request, pk):
        event = Event.objects.get(pk=pk)
        list_of_mentors = request.data.get('responses', [])

        for mentor in list_of_mentors:
            Register.objects.filter(
                event=event, mentor_id=mentor['mentor']).update(attended=mentor['attended'])

        serializer = self.serializer(instance=event)
        return Response(serializer.data)
