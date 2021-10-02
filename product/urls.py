from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductsList.as_view(), name='list'),
    path('<slug>', views.ProductDetails.as_view(), name='detail'),
    path('addtocart/', views.AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('shopresume/', views.ShopResume.as_view(), name='shopresume'),
]
