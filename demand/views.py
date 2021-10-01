from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse

# Create your views here.

class Pay(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pay')

class SaveDemand(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FinishDemand')

class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')