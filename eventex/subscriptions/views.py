from django.conf import settings
from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect
from django.views.generic import View
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from eventex.subscriptions.models import Subscription
from django.views.generic import DetailView

# def new(request):
#    if request.method == 'POST':
#       return create(request)
      
#    return empty_form(request)

# def empty_form(request):
#    return render(request,'subscriptions/subscription_form.html', {'form':SubscriptionForm()}) 

# def create(request):
#    form = SubscriptionForm(request.POST)

#    if not form.is_valid():
#       return render(request,'subscriptions/subscription_form.html',{'form':form})

#    #subscription = Subscription.objects.create(**form.cleaned_data)
#    subscription = form.save()

#    #Send subscription email

#    _send_email('Confirmação de inscrição',
#                settings.DEFAULT_FROM_EMAIL,
#                subscription.email,
#                'subscriptions/subscription_email.txt',
#                {'subscription': subscription})  
#    #Save in DB

#    # Success feddback - Não precisa mais devido a tela de agradecimento.
#    #messages.success(request,'Inscrição realizada com sucesso!')
         
#    return HttpResponseRedirect(r('subscriptions:detail',subscription.pk))

class SubscriptionCreate(View):
   def get(self, *args, **kwargs): # será o empty
      return render(self.request,'subscriptions/subscription_form.html', {'form':SubscriptionForm()}) 

   def post(self, *args, **kwargs): # será o create
      
      form = SubscriptionForm(self.request.POST)

      if not form.is_valid():
         return render(self.request,'subscriptions/subscription_form.html',{'form':form})
      
      subscription = form.save()

      #Send subscription email
      _send_email('Confirmação de inscrição',
                  settings.DEFAULT_FROM_EMAIL,
                  subscription.email,
                  'subscriptions/subscription_email.txt',
                  {'subscription': subscription})  
            
      return HttpResponseRedirect(r('subscriptions:detail',subscription.pk))   

new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])


