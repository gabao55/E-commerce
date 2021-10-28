from django.urls import path
from . import views

app_name = 'demand'

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('list/', views.List.as_view(), name='list'),
    path('savedemand/', views.SaveDemand.as_view(), name='savedemand'),
    path('detail/', views.Detail.as_view(), name='detail'),
]
