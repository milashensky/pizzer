from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from common.mixins import SerializedView, AuthRequierdMixin
from catalogue.models import Currency
from common.forms import CustomerForm, AddressForm
from common.utils import gen_password


class ContextApi(SerializedView):

    def get(self, request):
        user = request.user
        data = {
            'id': user.pk
        }
        if user.pk and hasattr(user, 'customer'):
            data.update({
                'confirmed': user.is_active,
                'email': user.email,
                'username': user.username,
                'currency': user.customer.currency_id
            })
        return data

    def patch(self, request):
        if request.user.pk and hasattr(request.user, 'customer'):
            request.user.customer.currency = Currency.objects.get(pk=self.data.get('currency'))
            request.user.customer.save()
            return {'state': True}
        self.status = 400
        return {'state': False}


class CustomerApi(AuthRequierdMixin, SerializedView):
    fields = ('id', 'user__email:email', 'phone', 'user__last_name:name')

    def get(self, request):
        return self.request.user.customer

    def put(self, request):
        form = CustomerForm(self.data, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return {'state': True}
        return {'state': False, 'errors': form.errors}

    def patch(self, request):
        user = request.user
        if not user.is_active:
            password = gen_password()
            self.data['old_password'] = password
            user.set_password(password)
        form = PasswordChangeForm(user=user, data=self.data)
        if form.is_valid():
            form.user.is_active = True
            user = form.save()
            login(request, user)
            update_session_auth_hash(request, user)
            return {'state': True}
        return {'state': False, 'errors': form.errors}


class DeliveryAddressApi(AuthRequierdMixin, SerializedView):
    fields = ('id', 'address', 'house', 'appartaments')

    def get(self, request):
        if hasattr(request.user.customer, 'delivery_address'):
            return request.user.customer.delivery_address
        return {}

    def put(self, request):
        instance = None
        if hasattr(request.user.customer, 'delivery_address'):
            instance = request.user.customer.delivery_address
        form = AddressForm(self.data, instance=instance)
        if form.is_valid():
            form.save()
            return {'state': True}
        return {'state': False, 'errors': form.errors}
