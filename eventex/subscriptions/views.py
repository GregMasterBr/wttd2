import imp
import django
from django.shortcuts import render
from django.http import HttpResponse
from eventex.subscriptions.forms import SubscriptionForm

def subscribe(request):
   context = {'form':SubscriptionForm()}
   return render(request,'subscriptions/subscription_form.html',context) 
