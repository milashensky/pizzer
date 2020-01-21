from django.core.serializers.json import Serializer as JSONSerializer, Deserializer

from common.fields import JsonField


class Serializer(JSONSerializer):
    """
    A fix on JSONSerializer in order to prevent stringifying JSONField data.
    """
    def handle_field(self, obj, field):
        if isinstance(field, JsonField):
            self._current[field.name] = field._get_val_from_obj(obj)
        else:
            return super().handle_field(obj, field)
