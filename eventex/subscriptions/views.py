import imp
import django
from django.shortcuts import render
from django.http import HttpResponse

def subscribe(request):
   return render(request,'subscriptions/subscription_form.html') 
