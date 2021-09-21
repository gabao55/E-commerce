from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models

# Create your views here.

class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetails(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ProductDetails')

class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddToCart')

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')

class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')

class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')