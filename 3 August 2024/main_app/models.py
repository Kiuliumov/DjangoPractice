from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

class AstronautManager(models.Manager):
    def get_missions_by_missions_count(self):
        return super().get_queryset().annotate(total_missions=models.Count('missions')).order_by('-total_missions', 'phone_number')



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

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    manufacturer = models.CharField(max_length=100)
    capacity = models.SmallPositiveIntegerField(validators=[MinValueValidator(0)])
    weight = models.FloatField(validators=[MinValueValidator(0)])
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)


class Mission(models.Model):
    name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=(('Planned, Planned'),
                                                     ('Ongoing', 'Ongoing'),
                                                     ('Completed', 'Completed')), default='Planned')
    launch_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL)

