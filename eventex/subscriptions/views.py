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
from django.views.generic.edit import ModelFormMixin, ProcessFormView

class SubscriptionCreate(TemplateResponseMixin, ModelFormMixin, ProcessFormView):
   template_name = 'subscriptions/subscription_form.html'
   form_class = SubscriptionForm

   def get(self, *args, **kwargs): # será o empty
      self.object = None
      return super().get(*args, **kwargs)

   def post (self, *args, **kwargs): # será o create
      self.object = None  
      return super().post(*args, **kwargs)
    
   def form_valid(self, form):      
      self.object = form.save()

      #Send subscription email
      _send_email('Confirmação de inscrição',
                  settings.DEFAULT_FROM_EMAIL,
                  self.object.email,
                  'subscriptions/subscription_email.txt',
                  {'subscription': self.object})  
            
      return HttpResponseRedirect(self.get_success_url()) 
   
new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])


