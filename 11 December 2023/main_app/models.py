from django.db import models
from django.db.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
# Create your models here.

class TennisPlayer(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(5)])
    birth_date = models.DateField()
    country = models.CharField(max_length=100, validators=[MinLengthValidator(2)])

