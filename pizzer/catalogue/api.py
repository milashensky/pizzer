from common.mixins import SerializedView
from catalogue.models import Currency


class CurrencyApi(SerializedView):
    fields = ('pk', 'code', 'name', 'symbol', 'rate', 'precision')

    def get(self, request):
        return Currency.objects.filter(is_active=True)
