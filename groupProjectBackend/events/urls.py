from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('events/', views.EventList.as_view()),
    path('events/<int:pk>/', views.EventDetail.as_view()),
    path('events/categories/', views.CategoryList.as_view()),
    path('events/categories/<str:category>/', views.CategoryDetail.as_view()),
    path('events/categories/<str:category>/events/',
         views.CategoryProjectList.as_view()),
    # path('events/<int:pk>/mentors', views.XXX.as_view()),
    # path('events/<int:pk>/mentors/register>', views.XXX.as_view()),
    path('responses/', views.MentorsRegisterList.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
