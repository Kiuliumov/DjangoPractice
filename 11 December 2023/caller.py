import os

import django
from django.db.models import Count, Avg, F, Q
from main_app.models import *

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


def get_tennis_players(search_string, search_country):

    if not search_string and not search_country:
        return ""

    query = Q()

    if search_string:
        query &= Q(name__icontains=search_string)

    if search_country:
        query &= Q(country=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    ret_str = ''
    for player in players:
        ret_str += f'Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}\n'
    return ret_str.rstrip()


def get_top_tennis_player():
    top_player = (TennisPlayer.objects
                  .annotate(wc=Count('winning_matches'))
                  .order_by('-wc', 'full_name')
                  .first())
    if not top_player:
        return ""
    return f'Top Tennis Player: {top_player.full_name} with {top_player.wc} wins.'


def get_tennis_player_by_matches_count():
    top_player = (TennisPlayer.objects
                  .annotate(m='matches_count')
                  .order_by("-m", "full_name")
                  .first()
                  )

    if not top_player or top_player.matches_count == 0:
        return ""

    return f'Tennis Player: {top_player.full_name} with {top_player.m} matches played."'
