from urllib import response
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from django.shortcuts import redirect, resolve_url as r
from django.core import mail


class SubscribeTest(TestCase):
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

        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_crsf(self):
        """Html must contain csrf_token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""

        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""

        form = self.response.context['form']
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
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

    def test_subscription_email_subject(self):
        ''''''
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        ''''''
        email = mail.outbox[0]
        expect = 'gregmasterbr+wttd@gmail.com'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        ''''''
        email = mail.outbox[0]
        expect = ['gregmasterbr+wttd@gmail.com', 'gregmasterbr@gmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        ''''''
        email = mail.outbox[0]
        self.assertIn('Gregorio Queiroz', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('gregmasterbr@gmail.com', email.body)
        self.assertIn('15-98105-7742', email.body)


class SubscribeInvalidPost(TestCase):
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
        response = self.client.post('/inscricao/',data,follow=True)
        self.assertContains(response,'Inscrição realizada com sucesso!')
