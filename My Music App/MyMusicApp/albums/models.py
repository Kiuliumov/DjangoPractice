from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class GenreChoices(models.TextChoices):
    POP = 'Pop Music'
    JAZZ = 'Jazz Music'
    RNB = 'R&B Music'
    COUNTRY = 'Country Music'
    DANCE = 'Dance Music'
    HIP_HOP = 'Hip Hop Music'
    OTHER = 'Other'

class Album(models.Model):
    name = models.CharField(max_length=30, unique=True)
    artist = models.CharField(max_length=30)
    genre = models.CharField(max_length=30, choices=GenreChoices.choices)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, null=True, blank=True, editable=False)
    
