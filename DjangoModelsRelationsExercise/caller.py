import os
from datetime import timedelta, date

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Review, Product, DrivingLicense, Driver, Owner, Car, Registration


def show_all_authors_with_their_books():
    result = []
    authors = Author.objects.all().order_by('id')
    for author in authors:
        # books = Book.objects.filter(author=author)
        books = author.book_set.all()
        if not books:
            continue
        titles = ', '.join(book.title for book in books)
        result.append(f"{author.name} has written - {titles}!")
    return '\n'.join(result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    if reviews:
        return sum(review.rating for review in reviews) / len(reviews)
    else:
        return 0
#     product = Product.objects.annotate(
#     total_ratings=Sum('reviews__rating'),
#     num_reviews=Count('reviews')
#     ).get(name=product_name)
#     return product.total_ratings / product.num_reviews


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()
    # or just get_products_with_no_reviews().delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    return '\n'.join(str(l) for l in licenses)


def get_drivers_with_expired_licenses(due_date):
    # so that we don't add timedelta for each driver in order to calculate whether his/her license is expired or not,
    # we find the cutoff date, where all licenses issued beforehand would be expired
    expiration_cutoff_date = due_date - timedelta(365)
    drivers_with_expired_licences = Driver.objects.filter(license__issue_date__gt=expiration_cutoff_date)
    return drivers_with_expired_licences


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()
    car.owner = owner
    car.save()
    registration.registration_date = date.today()
    registration.car = car
    registration.save()
    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."