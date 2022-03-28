from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages

def subscribe(request):
   if request.method == 'POST':
      form = SubscriptionForm(request.POST)
      #form.full_clean()
      if form.is_valid():
      # context = dict(name='Gregorio Queiroz', cpf='12345678901',
      #                  email='gregmasterbr@gmail.com', phone='15-98105-7742')

         body = render_to_string('subscriptions/subscription_email.txt',form.cleaned_data)

         mail.send_mail(
            'Confirmação de inscrição',
            body,
            'gregmasterbr+wttd@gmail.com',
            ['gregmasterbr+wttd@gmail.com',form.cleaned_data['email']]
         )
         messages.success(request,'Inscrição realizada com sucesso!')
         
         return HttpResponseRedirect('/inscricao/')
      else:
         return render(request,'subscriptions/subscription_form.html',{'form':form})
   else:
      context = {'form':SubscriptionForm()}
      return render(request,'subscriptions/subscription_form.html',context) 
