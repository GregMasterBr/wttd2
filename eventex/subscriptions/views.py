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
      self.send_email()
      return response

   def send_email(self):
      #Send subscription email
      subject = 'Confirmação de inscrição'
      from_ = settings.DEFAULT_FROM_EMAIL
      to_ = self.object.email 
      template_name = 'subscriptions/subscription_email.txt'
      context = {'subscription': self.object}

      body = render_to_string(template_name,context)
      return mail.send_mail(subject,body,from_,[from_, to_])            

new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)


