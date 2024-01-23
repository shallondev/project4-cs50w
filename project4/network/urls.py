
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>/", views.profile_view, name="profile_view"),
    path('following/<str:username>/', views.following_view, name='following_view'),
    path('edit/<int:posting>', views.edit, name='edit'),
]
