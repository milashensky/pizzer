import re

from django import forms
from django.contrib.auth.models import User

from common.models import Customer, DeliveryAddress


class PhoneValidator:

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not re.match(r'^\+?[-\s]?\(?[0-9]{1,2}\)?[-\s]?\(?([0-9]{3,4})\)?[-.\s]?([0-9]{2,3})[-.\s]?([0-9]{2,4})[-.\s]?([0-9]{2})?$', phone):
            raise forms.ValidationError('Invalid phone number')
        return phone


class CustomerForm(forms.ModelForm, PhoneValidator):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True, max_length=150)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exclude(id=self.instance.user_id).count():
            raise forms.ValidationError('Email already in use.')
        return email

    def save(self):
        self.instance.user.email = self.cleaned_data.get('email')
        self.instance.user.name = self.cleaned_data.get('name')
        self.instance.user.save()
        return super().save()

    class Meta:
        model = Customer
        fields = ('phone',)


class AddressForm(forms.ModelForm):

    class Meta:
        model = DeliveryAddress
        fields = ('appartaments', 'address', 'house')
