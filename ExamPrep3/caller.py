import os
import django
from django.db.models import Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''

    if search_name is not None and search_email is not None:
        authors = Author.objects.filter(full_name__icontains=search_name, email__icontains=search_email).order_by(
            '-full_name')

    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name).order_by('-full_name')

    else:
        authors = Author.objects.filter(email__icontains=search_email).order_by('-full_name')

    authors_info = []
    for author in authors:
        status = 'Banned' if author.is_banned else 'Not Banned'
        authors_info.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return "\n".join(authors_info) if authors_info else ''


def get_top_publisher():
    # the custom manager could be used here too
    top_author = (Author.objects
                  .annotate(article_count=Count('article')).filter(article_count__gt=0)
                  .order_by('-article_count', 'email')
                  .first())

    if not top_author:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.article_count} published articles."


def get_top_reviewer():
    top_reviewer = (Author.objects
                    .annotate(review_count=Count('review')).filter(review_count__gt=0)
                    .order_by('-review_count', 'email')
                    .first())

    if not top_reviewer:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if not latest_article:
        return ""

    authors = latest_article.authors.order_by('full_name')
    authors_names = [author.full_name for author in authors]

    review_count = latest_article.review_set.count()
    avg_rating = latest_article.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']

    if avg_rating is None:
        avg_rating = 0.00

    authors_str = ", ".join(authors_names)
    return (f"The latest article is: {latest_article.title}. Authors: {authors_str}. "
            f"Reviewed: {review_count} times. Average Rating: {avg_rating:.2f}.")


# def get_latest_article():
#     latest_article = Article.objects.prefetch_related('author_set', 'review_set').order_by('-published_on').first()
#
#     if latest_article is None:
#         return ""
#
#     authors_names = ', '.join(author.full_name for author in latest_article.authors.all().order_by('full_name'))
#     num_reviews = latest_article.reviews.count()
#     avg_rating = sum([r.rating for r in latest_article.reviews.all()]) / num_reviews if num_reviews else 0.0
#
#     return f"The latest article is: {latest_article.title}.
#     Authors: {authors_names}. Reviewed: {num_reviews} times." \
#            f" Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    top_rated_article = (Article.objects
                         .annotate(avg_rating=Avg('review__rating'))
                         .filter(avg_rating__isnull=False)
                         .order_by('-avg_rating', 'title')
                         .first())

    if not top_rated_article:
        return ""

    num_reviews = top_rated_article.review_set.count()
    avg_rating = top_rated_article.avg_rating

    return (f"The top-rated article is: {top_rated_article.title}, "
            f"with an average rating of {avg_rating:.2f}, reviewed {num_reviews} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    author = Author.objects.filter(email=email).first()

    if not author:
        return "No authors banned."

    num_reviews = Review.objects.filter(author=author).count()
    Review.objects.filter(author=author).delete()
    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."

# def ban_author(email=None):
#     if email is None:
#         return "No authors banned."

#     author = Author.objects.prefetch_related('review_set').filter(email=email).first()

#     if author is None:
#         return "No authors banned."
#
#     num_reviews = author.reviews.count()
#
#     author.is_banned = True
#     author.save()
#     author.reviews.all().delete()
#
#     return f"Author: {author.full_name} is banned! {num_reviews_deleted} reviews deleted."
