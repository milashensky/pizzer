from django.db import models


class Currency(models.Model):
    id = models.PositiveSmallIntegerField('ISO numeric', primary_key=True)
    code = models.CharField('Code (ISO)', max_length=4)
    name = models.CharField('Official name (CAPS)', max_length=128)
    symbol = models.CharField('Symbol', max_length=3, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rate = models.FloatField(default=1.0)
    precision = models.PositiveSmallIntegerField(default=100)

    class Meta:
        ordering = ('code', )
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return u'%s' % self.code

    def humanize(self, amount):
        return amount and (float(amount) / self.precision)

    def unhumanize(self, amount):
        return amount and (float(amount) * self.precision)


class Photo(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return str(self.created_at)
