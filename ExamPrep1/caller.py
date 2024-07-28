import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)
    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []
    for director in directors:
        result.append(f"Director: {director.full_name},"
                      f" nationality: {director.nationality},"
                      f" experience: {director.years_of_experience}")
    return "\n".join(result)


def get_top_director():
    top_director = (Director.objects.annotate(movie_count=Count('movie'))
                    .order_by('-movie_count', 'full_name').first())
    if top_director is None or top_director.movie_count == 0:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.movie_count}."


def get_top_actor():
    top_actor = (Actor.objects.annotate(starring_count=Count('starring_roles'))
                 .order_by('-starring_count', 'full_name').first())
    if top_actor is None or top_actor.starring_count == 0:
        return ""

    movies = top_actor.starring_roles.all()
    if not movies.exists():
        return ""

    movie_titles = ", ".join(movies.values_list('title', flat=True))
    avg_rating = movies.aggregate(Avg('rating'))['rating__avg']

    return (f"Top Actor: {top_actor.full_name},"
            f" starring in movies: {movie_titles},"
            f" movies average rating: {avg_rating:.1f}")


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('movies')).order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")
    return "\n".join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not top_movie:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    # participating = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    # cast = ', '.join(participating)
    cast = ", ".join(sorted(actor.full_name for actor in top_movie.actors.all()))

    return (f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. Cast: {cast}.")


def increase_rating():
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)
    num_of_updated_movies = classic_movies.update(rating=F('rating') + 0.1)

    if num_of_updated_movies == 0:
        return "No ratings increased."
    return f"Rating increased for {num_of_updated_movies} movies."