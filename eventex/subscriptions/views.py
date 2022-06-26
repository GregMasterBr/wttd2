from django.conf import settings
from django.shortcuts import render, resolve_url as r
from django.http import Http404, HttpResponseRedirect
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages
from eventex.subscriptions.models import Subscription

def new(request):
   if request.method == 'POST':
      return create(request)
      
   return empty_form(request)


def empty_form(request):
   return render(request,'subscriptions/subscription_form.html', {'form':SubscriptionForm()}) 


def create(request):
   form = SubscriptionForm(request.POST)

   if not form.is_valid():
      return render(request,'subscriptions/subscription_form.html',{'form':form})

   #subscription = Subscription.objects.create(**form.cleaned_data)
   subscription = form.save()

   #Send subscription email

   _send_email('Confirmação de inscrição',
               settings.DEFAULT_FROM_EMAIL,
               subscription.email,
               'subscriptions/subscription_email.txt',
               {'subscription': subscription})  
   #Save in DB

   # Success feddback - Não precisa mais devido a tela de agradecimento.
   #messages.success(request,'Inscrição realizada com sucesso!')
         
   return HttpResponseRedirect(r('subscriptions:detail',subscription.pk))


def detail(request,pk):
   try:
      subscription = Subscription.objects.get(pk=pk)
   except Subscription.DoesNotExist:
      raise Http404
   # subscription = Subscription(
   #    name='Gregorio Queiroz',
   #    cpf='12345678901',
   #    email='gregmasterbr@gmail.com',
   #    phone='15-981057742'
   # )
   return render(request, 'subscriptions/subscription_detail.html', {'subscription': subscription})

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])
