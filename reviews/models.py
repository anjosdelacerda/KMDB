from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RecomendationOptions(models.TextChoices):
    MUST_WATCH = "Must Watch"
    SHOULD_WATCH = "Should Watch"
    AVOID_WATCH = "Avoid Watch"
    NO_OPINION = "No Opinion"


class Review(models.Model):
    review = models.TextField()
    spoilers = models.BooleanField(default=False)
    recomendation = models.CharField(
        max_length=50, choices=RecomendationOptions.choices, default=RecomendationOptions.NO_OPINION)

    stars = models.IntegerField(
        validators=[MaxValueValidator(10),
         MinValueValidator(1)],)
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="reviews")
    critic = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews")
