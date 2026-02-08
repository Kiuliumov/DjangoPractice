from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator:
    message = "The phone number must contain only digits!"

    def __init__(self, message: str = None):
        if message:
            self.message = message

    def __call__(self, value: str):
        if not value.isdigit():
            raise ValidationError(self.message)


class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[PhoneNumberValidator()],
        unique=True
    )
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    spacewalks = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    updated_at = models.DateTimeField(auto_now=True)



class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.SmallPositiveIntegerField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
