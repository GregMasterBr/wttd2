from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Gregorio Queiroz',
            cpf='12345678910',
            email='gregmasterbr@gmail.com',
            phone='15-981057742'
        )
        self.obj.save()        

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        ''''Subscriprion must have an auto created_at attr.'''
        self.assertIsInstance(self.obj.created_at, datetime)        