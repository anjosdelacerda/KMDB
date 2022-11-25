from django.urls import path

from . import views

urlpatterns = [
    path('users/register/', views.UserView.as_view()),
    path('users/login/', views.LoginView.as_view()),
    path('users/', views.UserGetListView.as_view()),
    path('users/<int:user_id>/', views.UserGetIdView.as_view())
]
