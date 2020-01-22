import os
import hmac
import time
import random
import hashlib

from django.contrib.auth.models import User


def upload_to(instance, filename):
    name, ext = filename.rsplit('.', 1)
    key, msg = str(random.randint(1, 100000)), str(instance.pk)
    filename = u'{0:s}.{1:s}'.format(hmac.new(key.encode(), msg.encode()).hexdigest(), ext)
    return os.path.join(instance._meta.app_label, instance._meta.model_name, filename)


def gen_password():
    return hashlib.md5(str(time.time()).encode()).hexdigest()


def create_temporary_user(email):
    return User.objects.create(email=email, username=email, password=gen_password(), is_active=False)
