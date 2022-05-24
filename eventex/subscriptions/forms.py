from django.core.exceptions import ValidationError
from django import forms

def validate_cpf(value):
    if not value.isdigit():
        raise forms.ValidationError('CPF deve conter apenas números','digits')

    if len(value) != 11:
        raise forms.ValidationError('CPF deve conter 11 números','length')

class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')

    def clean_name(self):
        name = self.cleaned_data['name']

        words = [w.capitalize() for w in name.split()]

        return ' '.join(words)