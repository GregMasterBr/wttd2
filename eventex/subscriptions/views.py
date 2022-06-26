from django.conf import settings
from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect
from django.views.generic import View
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from eventex.subscriptions.models import Subscription
from django.views.generic import CreateView, DetailView

class SubscriptionCreate(CreateView):
   model = Subscription
   form_class = SubscriptionForm

   def form_valid(self, form):      
      response = super().form_valid(form)

      #Send subscription email
      _send_email('Confirmação de inscrição',
                  settings.DEFAULT_FROM_EMAIL,
                  self.object.email,
                  'subscriptions/subscription_email.txt',
                  {'subscription': self.object})  
            
      return response
   
new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])


