from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, resolve_url as r
from django.http import HttpResponseRedirect
from django.views.generic import View
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from eventex.subscriptions.models import Subscription
from django.views.generic import DetailView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormMixin

class SubscriptionCreate(TemplateResponseMixin, FormMixin, View):
   template_name = 'subscriptions/subscription_form.html'
   form_class = SubscriptionForm

   def get(self, *args, **kwargs): # será o empty
      self.object = None
      return self.render_to_response(self.get_context_data())

   def post (self, *args, **kwargs): # será o create
      self.object = None      
      form = self.get_form()

      if not form.is_valid():
         return self.form_invalid(form)
      return self.form_valid(form)

   def form_valid(self, form):      
      self.object = form.save()

      #Send subscription email
      _send_email('Confirmação de inscrição',
                  settings.DEFAULT_FROM_EMAIL,
                  self.object.email,
                  'subscriptions/subscription_email.txt',
                  {'subscription': self.object})  
            
      return HttpResponseRedirect(self.get_success_url()) 
   
   def get_success_url(self):
      return self.object.get_absolute_url()
   
new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])


