from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.managers import DirectorManager
from main_app.mixins import FullNameBirthDateNationalityMixin, IsAwardedLastUpdatedMixin


# Create your models here.
class Director(FullNameBirthDateNationalityMixin):
    years_of_experience = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

    objects = DirectorManager()


class Actor(FullNameBirthDateNationalityMixin, IsAwardedLastUpdatedMixin):
    pass


class Movie(IsAwardedLastUpdatedMixin):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=6, choices=GENRE_CHOICES, default='Other')
    rating = models.DecimalField(max_digits=3,
                                 decimal_places=1,
                                 default=0.0,
                                 validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    starring_actor = models.ForeignKey(Actor,
                                       null=True,
                                       on_delete=models.SET_NULL,
                                       related_name='starring_roles')
    actors = models.ManyToManyField(Actor, related_name='movies')

