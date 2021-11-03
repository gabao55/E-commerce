from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('', views.Create.as_view(), name='create'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('reset-password/', views.ForgotPassword.as_view(), name='password_reset'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
]
