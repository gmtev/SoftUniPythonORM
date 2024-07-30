from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator, DecimalValidator
from django.db.models import Count


class TennisPlayerManager(models.Manager):
    def get_tennis_players_by_wins_count(self):
        return self.annotate(wins_count=Count('matches_won')).order_by('-wins_count', 'full_name')


class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)]
    )
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(300)]
    )
    is_active = models.BooleanField(default=True)
    objects = TennisPlayerManager()


class Tournament(models.Model):
    SURFACE_CHOICES = [
        ('Not Selected', 'Not Selected'),
        ('Clay', 'Clay'),
        ('Grass', 'Grass'),
        ('Hard Court', 'Hard Court'),
    ]

    name = models.CharField(
        max_length=150,
        unique=True,
        validators=[MinLengthValidator(2)]
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[DecimalValidator(max_digits=10, decimal_places=2)]
    )
    start_date = models.DateField()

    surface_type = models.CharField(
        max_length=12,
        choices=SURFACE_CHOICES,
        default='Not Selected'
    )


class Match(models.Model):
    score = models.CharField(
        max_length=100
    )
    summary = models.TextField(
        validators=[MinLengthValidator(5)]
    )
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE
    )
    players = models.ManyToManyField(TennisPlayer)
    winner = models.ForeignKey(
        TennisPlayer,
        on_delete=models.SET_NULL,
        null=True,
        related_name='matches_won'
    )

    class Meta:
        verbose_name_plural = "Matches"
