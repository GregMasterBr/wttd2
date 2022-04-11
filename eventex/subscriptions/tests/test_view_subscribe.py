from urllib import response
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.shortcuts import redirect, resolve_url as r
from django.core import mail


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        '''
        GET /inscricao must return status code 200
        '''
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        '''
        Must use subscriptions/subscription_form.html
        '''
        self.assertTemplateUsed(
            self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ Html must contaim input tags"""
        tags = (('<form',1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"',1),
                ('type="submit"',1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text,count)

        # self.assertContains(self.response, '<form')
        # self.assertContains(self.response, '<input', 6)
        # self.assertContains(self.response, 'type="text"', 3)
        # self.assertContains(self.response, 'type="email"',1)
        # self.assertContains(self.response, 'type="submit"',1)

    def test_crsf(self):
        """Html must contain csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""

        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
        data = dict(name='Gregorio Queiroz', cpf='12345678901',
                    email='gregmasterbr@gmail.com', phone='15-98105-7742')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        '''
            Valid POST should redirect to /inscricao/
        '''
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe_email(self):
        ''' Valida se existe o e-mail   '''
        self.assertEqual(1, len(mail.outbox))           

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name='Gregorio Queiroz', cpf='12345678901',
                    email='gregmasterbr@gmail.com', phone='15-98105-7742')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
