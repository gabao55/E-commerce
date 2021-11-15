from django import http
from django.contrib.auth.models import User
from django.contrib.messages.api import error
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models
from user.models import UserProfile
import json
from django.core import serializers
from django.db.models import Q
# Create your views here.

class ProductsList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']

class Search(ProductsList):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        qs = super().get_queryset(*args, **kwargs)

        if not term:
            return qs

        self.request.session['term'] = term

        qs = qs.filter(
            Q(name__icontains=term) |
            Q(short_description__icontains=term) |
            Q(large_description__icontains=term)
        )

        self.request.session.save()

        return qs
class ProductDetails(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

class AddToCart(View):
    def get(self, *args, **kwargs):
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'The product does not exist.'
            )

            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_inventory = variation.inventory
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        unit_promotional_price = variation.promotional_price
        amount = 1
        slug = product.slug
        image = json.dumps(str(product.image))
        image_url = json.loads(image)

        if variation.inventory <1:
            messages.error(
                self.request,
                'Out of product.'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            # TODO: variation exists in the cart
            cart_amount = cart[variation_id]['amount']
            cart_amount += 1

            if variation_inventory < cart_amount:
                messages.warning(
                    self.request,
                    f'Out of inventory for {cart_amount}x in product "{product_name}". '
                    f'We added {variation_inventory}x the product in your cart.'
                )
                cart_amount = variation_inventory
            
            cart[variation_id]['amount'] = cart_amount
            cart[variation_id]['quantitative_price'] = unit_price * cart_amount
            cart[variation_id]['quantitative_promotional_price'] = unit_promotional_price * cart_amount

        else:
            cart[variation_id] = {
                'product_id' : product_id,
                'product_name' : product_name,
                'variation_name' : variation_name,
                'variation_id' : variation_id,
                'unit_price' : unit_price,
                'unit_promotional_price' : unit_promotional_price,
                'quantitative_price' : unit_price,
                'quantitative_promotional_price' : unit_promotional_price,
                'amount' : amount,
                'slug' : slug,
                'image' : image,
                'image_url' : image_url
            }

        self.request.session.save()
        messages.success(
            self.request,
            f'Product {product_name} {variation_name} added to the cart '
            f'{cart[variation_id]["amount"]}x.'
        )

        return redirect(http_referer)

class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Product "{cart["product_name"]} {cart["variation_name"]} removed from cart."'
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)

class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart' : self.request.session.get('cart', {})
        }
        return render(self.request, 'product/cart.html', context)

class ShopResume(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:login')

        profile = UserProfile.objects.filter(user=self.request.user).exists()

        if not profile:
            messages.error(
                self.request,
                'User without profile.'
            )
            return redirect('user:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }
        return render(self.request, 'product/shopresume.html', context)

# class CreateCheckoutSessionView(View):
#     def