from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from product.models import Variation
from utils import utils
from .models import Demand, DemandItem
import json
# Create your views here.

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('user:login')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        
        return qs

class Pay(DispatchLoginRequiredMixin, DetailView):
    #TODO: Add payment method (Use stripe)
    # tutorial:  https://www.youtube.com/watch?v=oZwyA9lUwRk&ab_channel=DennisIvy
    template_name = 'demand/pay.html'
    model = Demand
    pk_url_kwarg = 'pk'
    context_object_name = 'demand'


class SaveDemand(View):

    template_name = 'demand/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You have to be login to finish your purchase.'
            )
            return redirect('user:login')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('product:list')


        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variation_ids)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            inventory = variation.inventory
            cart_amount = cart[vid]['amount']
            unit_price = cart[vid]['unit_price']
            unit_promotional_price = cart[vid]['unit_promotional_price']

            error_msg_inventory = ''
            
            if inventory < cart_amount:
                cart[vid]['amount'] = inventory
                cart[vid]['quantitative_price'] = inventory*unit_price
                cart[vid]['quantitative_promotional_price'] = inventory*unit_promotional_price

                error_msg_inventory = 'Some products you chose might not have the amount you wish in inventory. '\
                    'Amounts updated according to the inventory, please verify your new amounts.'

            if error_msg_inventory:
                messages.error(
                    self.request,
                    error_msg_inventory
                )
                
                self.request.session.save()
                return redirect('product:cart')

        cart_total_amount = utils.cart_total_amount(cart)
        cart_total_value = utils.cart_totals(cart)

        demand = Demand(
            user=self.request.user,
            total=cart_total_value,
            total_amount=cart_total_amount,
            status='C',
        )

        demand.save()

        DemandItem.objects.bulk_create(
            [
                DemandItem(
                    demand=demand,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['quantitative_promotional_price'],
                    amount=v['amount'],
                    image=json.loads(v['image']),
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'demand:pay',
                kwargs={
                    'pk': demand.pk
                }
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Demand
    context_object_name = 'demand'
    template_name = 'demand/detail.html'
    pk_url_kwarg = 'pk'

class List(DispatchLoginRequiredMixin, ListView):
    model = Demand
    context_object_name = 'demands'
    template_name = 'demand/list.html'
    paginate_by = 10
    ordering = ['-id']