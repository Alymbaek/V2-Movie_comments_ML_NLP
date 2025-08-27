from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField



class Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(16), MaxValueValidator(100)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')
    STATUS_CHOICES = (
        ('pro', 'Pro'),
        ('simple', 'Simple'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.username


class Country(models.Model):
   country_name = models.CharField(max_length=35, unique=True)

   def __str__(self):
       return self.country_name

class Director(models.Model):
    director_name = models.CharField(max_length=35)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0)
    director_image = models.ImageField(upload_to='director_image/')

    def __str__(self):
        return self.director_name


class Actor(models.Model):
    actor_name = models.CharField(max_length=35)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_image/', null=True, blank=True)

    def __str__(self):
        return self.actor_name

class Janre(models.Model):
    janre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.janre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='movie')
    director = models.ManyToManyField(Director, related_name='movie')
    actor = models.ManyToManyField(Actor, related_name='movie', verbose_name='Actors and Actress')
    janre = models.ManyToManyField(Janre, related_name='movie')
    TYPES_CHOICES = (
        ('144p', '144p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
    )
    types = MultiSelectField(choices=TYPES_CHOICES, max_choices=5, max_length=50, default='720p')
    movie_time = models.PositiveSmallIntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    movie_trailer = models.FileField(upload_to='movie_trailer', null=True, blank=True)
    movie_image = models.ImageField(upload_to='movie_image')
    STATUS_CHOICES = (
        ('pro', 'Pro'),
        ('simple', 'Simple'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return self.movie_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class MovieLanguages(models.Model):
    language = models.CharField(max_length=35)
    video = models.FileField(upload_to='MovieLanguages_video/')
    movie = models.ForeignKey(Movie, related_name='movie_languages', on_delete=models.CASCADE)

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, related_name='moments', on_delete=models.CASCADE)
    movie_moments = models.ImageField(upload_to='movie_moments')

    def __str__(self):
        return f'{self.movie_moments}'

class Rating(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,11)], verbose_name='Рейтинг')
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.movie} - {self.stars} stars'


class Favorite(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, related_name='favorite_movie', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cart}'

class History(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.movie}'