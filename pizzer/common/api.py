from django.contrib.auth.models import User

from common.mixins import SerializedView, AuthRequierdMixin
from catalogue.models import Currency


class ContextApi(SerializedView):

    def get(self, request):
        user = request.user
        data = {
            'id': user.pk
        }
        if user.pk and hasattr(user, 'customer'):
            data.update({
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


class Users(AuthRequierdMixin, SerializedView):
    fields = ('id', 'username')

    def get(self, request):
        page = int(request.GET.get('page', 0))
        per_page = int(request.GET.get('per_page', 20))
        current = page * per_page
        qs = User.objects.all().exclude(id=request.user.id)
        return {'users': self.serialize_items(qs[current:current + per_page], self.fields), 'count': qs.count()}
