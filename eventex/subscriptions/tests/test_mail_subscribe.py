from django.test import TestCase
from django.shortcuts import redirect, resolve_url as r
from django.core import mail


class SubscribeEmail(TestCase):
    def setUp(self):
        data = dict(name='Gregorio Queiroz', cpf='12345678901',
                    email='gregmasterbr@gmail.com', phone='15-98105-7742')
        self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        ''''''
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        ''''''
        expect = 'gregmasterbr+wttd@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        ''''''
        expect = ['gregmasterbr+wttd@gmail.com', 'gregmasterbr@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
                'Gregorio Queiroz',
                '12345678901',
                'gregmasterbr@gmail.com',
                '15-98105-7742'
        ]
        for content in contents:
            with self.subTest():
               self.assertIn(content, self.email.body)
