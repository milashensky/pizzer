from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    currency = models.ForeignKey('catalogue.Currency', default=840, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id

    @property
    def serialized(self):
        return {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email
        }


class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="delivery_addresses")
    details = models.TextField()

    def __str__(self):
        return 'customer %s: %s' % (self.customer_id, self.details[:15])
