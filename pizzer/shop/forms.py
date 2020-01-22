import logging

from django import forms
from django.contrib.auth.models import User

from shop.models import Order, ProductOrder, Product
from common.models import Customer, DeliveryAddress
from common.utils import create_temporary_user
from common.forms import PhoneValidator
from shop.utils import convert_price, get_delivery_price

logger = logging.getLogger(__name__)


class CreateOrderForm(forms.ModelForm, PhoneValidator):
    address = forms.CharField(required=True)
    house = forms.CharField(required=True)
    appartaments = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True, max_length=150)

    def clean(self):
        self.errors.pop('customer', None)
        self.errors.pop('total_price', None)
        self.errors.pop('customer_data', None)
        self.errors.pop('products_data', None)
        self.errors.pop('delivery_data', None)
        self.errors.pop('products_price', None)
        self.errors.pop('delivery_address', None)
        self.errors.pop('currency', None)
        self.clean_customer()
        self.clean_products()
        self.clean_delivery_address()
        # customer
        # products
        return self.cleaned_data

    def clean_customer(self):
        customer = None
        user = self.data.get('user')
        email = self.cleaned_data.get('email', '')
        name = self.cleaned_data.get('name')
        currency = self.cleaned_data.get('currency')
        phone = self.cleaned_data.get('phone')
        if not currency:
            return
        if not user.is_authenticated:
            if email:
                user = User.objects.filter(email=email).first()
                if not user:
                    user = create_temporary_user(email)
            if user.last_name is not name:
                user.last_name = name
                user.save()
        customer, cr = Customer.objects.get_or_create(user=user)
        ch = False
        if customer.currency_id is not currency.id:
            ch = True
            customer.currency = currency
        if phone and not customer.phone == phone:
            ch = True
            customer.phone = phone
        if ch:
            customer.save()
        self.data['user_created'] = cr
        self.data['user'] = user
        self.cleaned_data['customer'] = customer
        self.cleaned_data['customer_data'] = {
            'email': email,
            'name': name,
            'phone': phone
        }
        return customer

    def clean_email(self):
        user = self.data.get('user')
        email = self.cleaned_data.get('email', '')
        if user and user.is_authenticated and not user.email == email:
            email_user = User.objects.filter(email=email).first()
            if email_user:
                raise forms.ValidationError('Email already in use.')
            else:
                user.email = email
                user.save()
        return email

    def clean_products(self):
        self.errors.pop('products', None)
        products = self.data.get('products')
        currency = self.cleaned_data.get('currency')
        orders = []
        products_price = 0
        products_data = []
        if currency:
            for product_id, quantity in products:
                product = Product.objects.get(id=product_id)
                products_price += convert_price(product.price, currency, product.currency) * int(quantity)
                order = ProductOrder.objects.create(product=product, quantity=quantity)
                orders.append(order)
                products_data.append(order.serialized)
            self.cleaned_data['products_data'] = products_data
            self.cleaned_data['products_price'] = products_price
            self.cleaned_data['total_price'] = products_price + get_delivery_price(products_price, currency)
            self.cleaned_data['products'] = orders
        return products

    def clean_delivery_address(self):
        customer = self.cleaned_data.get('customer')
        if not customer:
            return
        address = {
            'address': self.cleaned_data['address'],
            'house': self.cleaned_data['house'],
            'appartaments': self.cleaned_data['appartaments']
        }
        if not hasattr(customer, 'delivery_address'):
            DeliveryAddress.objects.create(customer=customer, **address)
        else:
            DeliveryAddress.objects.filter(customer_id=customer.id).update(**address)
        self.cleaned_data['delivery_data'] = address
        self.cleaned_data['delivery_address'] = customer.delivery_address
        return customer.delivery_address

    def save(self):
        res = super().save()
        products = self.cleaned_data.get('products')
        for product in products:
            product.order = res
            product.save()
        return res

    class Meta:
        model = Order
        fields = (
            'customer', 'customer_data', 'products_data', 'details', 'currency', 'products_price',
            'total_price', 'delivery_address', 'delivery_data', 'payment_method'
        )
