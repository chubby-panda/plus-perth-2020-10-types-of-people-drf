from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/register/', views.CustomUserCreate.as_view()),
    path('users/<str:username>/', views.CustomUserDetail.as_view()),
    path('users/<str:username>/update-password/', views.ChangePasswordView.as_view()),
    path('users/mentor/<str:username>/profile/', views.MentorProfileDetail.as_view()),
    path('users/org/<str:username>/profile/', views.OrgProfileDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)