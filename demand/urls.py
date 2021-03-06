from django.urls import path
from . import views

app_name = 'demand'

urlpatterns = [
    path('pay/<int:pk>', views.Pay.as_view(), name='pay'),
    path('list/', views.List.as_view(), name='list'),
    path('savedemand/', views.SaveDemand.as_view(), name='savedemand'),
    path('detail/<int:pk>', views.Detail.as_view(), name='detail'),
]
