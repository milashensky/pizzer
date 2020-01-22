import json
import uuid
import logging
import datetime
from collections import OrderedDict, Iterable

from django.db import models
from django.http import HttpResponse
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseNotAllowed
from django.views.generic import View
from django.db.models.query import QuerySet
from django.db.models.fields.files import ImageFieldFile


logger = logging.getLogger(__name__)


class AuthRequierdMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'customer'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class DjangoJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, HttpResponse):
            return obj.content.decode()
        if isinstance(obj, ImageFieldFile):
            return {'url': obj.url, 'name': obj.name, 'path': obj.path}
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M')
        elif isinstance(obj, (datetime.datetime, datetime.date)):
            return str(obj.strftime('%s'))
        elif isinstance(obj, QuerySet):
            # + support of ValuesQuerySet
            return json.loads(serialize('json', obj)) if obj._fields is None else list(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, dict):
            return OrderedDict(obj)
        elif hasattr(obj, 'capitalize'):
            return obj.capitalize()
        return json.JSONEncoder.default(self, obj)


def JsonResponse(context, status=200):
    content = DjangoJSONEncoder().encode(context)
    return HttpResponse(content, content_type='application/json', status=status)


class JsonResponseMixin(object):
    status = 200

    def render_to_response(self, context):
        return JsonResponse(context, status=self.status)


class SerializedView(JsonResponseMixin, View):
    data = {}
    without_null = False

    def dispatch(self, request, *args, **kwargs):
        if not self.data:
            self.data = json.loads(request.body.decode('utf-8') or '{}')
        self.filter_data = {}
        for k, v in request.GET.dict().items():
            self.filter_data[k] = v.split(',') if v else []
        response = super(SerializedView, self).dispatch(
            request, *args, **kwargs)
        fields = getattr(self, 'fields', None)
        if isinstance(response, (HttpResponseNotAllowed, HttpResponse)):
            return response
        elif isinstance(response, models.Model):
            response = self.serialize_item(response, fields)
        elif not isinstance(response, dict) and fields:
            response = self.serialize_items(response, fields, self.without_null)
        return self.render_to_response(response)

    @staticmethod
    def serialize_items(data, fields, without_null=False):
        if isinstance(data, Iterable):
            items, data = list(data), []
            for item in items:
                if not isinstance(item, dict):
                    item = SerializedView.serialize_item(item, fields, without_null)
                data.append(item)
        return data

    @staticmethod
    def serialize_item(item, fields, without_null=False):
        obj = {}
        for field in fields:
            if isinstance(field, dict):
                for nest, nest_fields in field.items():
                    alias, attr = SerializedView.get_item_attr(item, nest)
                    if attr is None and without_null:
                        continue
                    if isinstance(attr, Iterable):
                        obj[alias] = SerializedView.serialize_items(attr, nest_fields, without_null=False)
                    else:
                        obj[alias] = SerializedView.serialize_item(attr, nest_fields, without_null=False)
                continue
            alias, attr = SerializedView.get_item_attr(item, field)
            if attr is None and without_null:
                continue
            obj[alias] = attr
        return obj

    @staticmethod
    def get_item_attr(item, field):
        alias = field
        if ':' in field:
            parts = field.split(':')
            field = parts[0]
            alias = parts[1]
        attr = item
        for a in field.split('__'):
            attr = getattr(attr, a, None)
            if callable(attr):
                if hasattr(attr, 'all') and callable(getattr(attr, "all")):
                    attr = getattr(attr, "all")()
                else:
                    attr = attr()
        return (alias, attr)
