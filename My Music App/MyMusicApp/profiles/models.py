from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
# Create your models here.

@deconstructible
class UserNameValidator:
    def __init__(self, message=None):
        self.message = message or "Ensure this value contains only letters, numbers, and underscore."
    
    def __call__(self, value):
        if not value.isalnum() and '_' not in value:
            raise ValidationError(self.message)

class Profile(models.Model):
    username = models.CharField(max_length=15, validators=[MinLengthValidator(2), UserNameValidator()])
    email = models.EmailField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
