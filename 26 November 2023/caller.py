import os
import django
from main_app.models import *
from django.db.models import Count, Avg, Q

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions

def get_authors(search_name=None, search_email=None):
    if not search_name and not search_email:
        return ""
    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)

    if search_email:
        query &= Q(email__icontains=search_email)
    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ''
    lines = [f'Author: {author.full_name}, email: {author.email}, status: {"Banned" if author.is_banned else "Not Banned"}' for author in authors]
    return '\n'.join(lines)

def get_top_publisher():
    top_publisher = Author.objects.annotate(article_count=Count('articles')).order_by('-article_count', 'email').first()

    if not top_publisher or top_publisher.article_count == 0:
        return ''

    return f'Top Author: {top_publisher.full_name} with {top_publisher.article_count} published articles.'

def get_top_reviewer():
    top_reviewer = Author.objects.annotate(review_count=Count('reviews')).order_by('-review_count', 'email').first()
    if not top_reviewer or top_reviewer.review_count == 0:
        return ''
    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.review_count} published reviews.'

def get_latest_article():
    latest_article = (
        Article.objects
        .order_by('-date_published')
        .annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        )
        .first()
    )

    if not latest_article:
        return ''

    return (
        f'The latest article is: {latest_article.title}. '
        f'Authors: {", ".join(a.full_name for a in latest_article.authors.all())}. '
        f'Reviewed: {latest_article.review_count} times. '
        f'Average Rating: {latest_article.avg_rating or 0:.2f}.'
    )

def get_top_rated_article():

    top_rated_article = (Article.objects
                        .annotate(review_count=Count('reviews'), avg_rating=Avg('reviews__rating'))
                        .order_by('-avg_rating', 'title')
                        .first())

    if not top_rated_article:
        return ''

    if not top_rated_article.reviews.exists():
        return ''

    return f'The top-rated article is: {top_rated_article.title}, with an average rating of {top_rated_article.avg_rating}, reviewed {top_rated_article.review_count} times.'

def ban_author(email=None):
    if not email:
        return 'No authors banned.'
    author = Author.objects.filter(email__iexact=email).annotate(reviews_count=Count('reviews')).first()

    if not author:
        return 'No authors banned.'

    reviews_count = author.reviews_count
    author.is_banned = True
    author.reviews.all().delete()

    author.save()
    return f'Author: {author.full_name} is banned! {reviews_count} reviews were deleted. '