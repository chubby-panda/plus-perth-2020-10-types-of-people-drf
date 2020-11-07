from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/most-popular/', views.PopularEventsList.as_view()),
    path('events/most-popular/short-list/',
         views.PopularEventsShortList.as_view()),
    path('events/location/<int:kms>/', views.LocationEventsList.as_view()),
    path('events/<int:pk>/responses/', views.MentorsRegisterList.as_view()),
    #adding new url to allow org to mark attendane
    path('events/<int:pk>/attendance/', views.EventAttendenceView.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
    path('events/categories/', views.CategoryList.as_view()),
    path('events/categories/<str:category>/', views.CategoryDetail.as_view()),
    path('events/categories/<str:category>/events/',
         views.CategoryProjectList.as_view()),
    path('events/categories/<str:category>/events/short-list/',
         views.CategoryProjectShortList.as_view()),
    path('events/<str:username>/mentor-attendance/',
         views.MentorAttendanceView.as_view()),
    path('events/<str:username>/events-hosted/',
         views.EventHostedView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)