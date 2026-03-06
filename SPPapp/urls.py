from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
   path('', views.home, name='home'),
    path('predict/', views.predict_view, name='predict'),
    path('history/', views.prediction_history, name='history'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
