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

class SubscriptionCreate(TemplateResponseMixin, View):
   template_name = 'subscriptions/subscription_form.html'
   form_class = SubscriptionForm

   def get(self, *args, **kwargs): # será o empty
      return self.render_to_response(self.get_context_data())

   # def post(self, *args, **kwargs): # será o create
      
   #    form = SubscriptionForm(self.request.POST)

   #    if not form.is_valid():
   #       return render(self.request, self.template_name,{'form':form})
      
   #    subscription = form.save()

   #    #Send subscription email
   #    _send_email('Confirmação de inscrição',
   #                settings.DEFAULT_FROM_EMAIL,
   #                subscription.email,
   #                'subscriptions/subscription_email.txt',
   #                {'subscription': subscription})  
            
   #    return HttpResponseRedirect(r('subscriptions:detail',subscription.pk))   

   def post (self, *args, **kwargs): # será o create
      
      form = self.get_form()

      if not form.is_valid():
         return self.form_invalid(form)
      return self.form_valid(form)

   def form_invalid(self, form):
      return self.render_to_response(self.get_context_data(form=form))
      
   def form_valid(self, form):      
      subscription = form.save()

      #Send subscription email
      _send_email('Confirmação de inscrição',
                  settings.DEFAULT_FROM_EMAIL,
                  subscription.email,
                  'subscriptions/subscription_email.txt',
                  {'subscription': subscription})  
            
      return HttpResponseRedirect(subscription.get_absolute_url()) 

   def get_form(self):
      if self.request.method == 'POST':
         return self.form_class(self.request.POST)
      return self.form_class()

   def get_context_data(self, **kwargs):
      context = dict(kwargs)
      context.setdefault('form', self.get_form())
      return context 

new =  SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)

def _send_email(subject, from_,to_,template_name,context):
   body = render_to_string(template_name,context)
   mail.send_mail(subject,body,from_,[from_, to_])


