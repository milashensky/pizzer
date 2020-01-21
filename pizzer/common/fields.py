import json
import logging

from django.db import models

logger = logging.getLogger(__name__)


class JsonField(models.TextField):

    def to_python(self, value):
        return value

    def from_db_value(self, value, *args, **kwargs):
        return json.loads(value)

    def get_prep_value(self, value):
        return super().get_prep_value(json.dumps(value))

    def _get_val_from_obj(self, obj):
        return getattr(obj, self.attname)
