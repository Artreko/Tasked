from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField, BinaryField
from .utils.key_generator.generate_key_file import make_encrypted_message
from .utils.key_reader.check_key import decrypt_message
# Create your models here.


class EncyptedCharField(CharField):
    description = "Encrypted sin value"

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = True
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        # encrypt data with your own function
        return make_encrypted_message(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # decrypt data with your own function
        return decrypt_message(value)

    def to_python(self, value):
        if isinstance(value, Task):
            return value
        if value is None:
            return value
        # print(value)
        # decrypt data with your own function
        return value

class EncyptedTextField(CharField):
    description = "Encrypted sin value"

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = True
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        # encrypt data with your own function
        if value is None:
            return value
        return make_encrypted_message(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return ''
        # decrypt data with your own function
        return decrypt_message(value)

    def to_python(self, value):
        if isinstance(value, Task):
            return value
        if value is None:
            return ''
        # print(value)
        return value


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = EncyptedCharField()
    description = EncyptedTextField()
    complete = models.BooleanField(default=False)
    deadline = models.DateField(blank=True, null=True)


    class Meta:
        order_with_respect_to = 'user'
