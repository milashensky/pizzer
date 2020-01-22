from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    phone = models.CharField(max_length=128)
    currency = models.ForeignKey('catalogue.Currency', default=840, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s: %s' % (self.user_id, self.created_at)

    @property
    def serialized(self):
        return {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email
        }


class DeliveryAddress(models.Model):
    address = models.TextField()
    house = models.CharField(max_length=128)
    appartaments = models.CharField(max_length=70)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="delivery_address", null=True)

    def __str__(self):
        return '%s, %s, %s' % (self.address, self.house, self.appartaments)
