import os

import django
from django.db.models import Count, Avg, F, Q
from main_app.models import *

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions


def get_tennis_players(search_name=None, search_country=None):
    if not search_name and not search_country:
        return ""

    query = Q()
    if search_name:
        query &= Q(full_name__icontains=search_name)
    if search_country:
        query &= Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return ""

    ret_str = ""
    for player in players:
        ret_str += f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}\n"
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
    top_player = (
        TennisPlayer.objects
        .annotate(m=Count("matches"))
        .order_by("-m", "ranking")
        .first()
    )

    if not top_player or top_player.m == 0:
        return ""

    return f"Tennis Player: {top_player.full_name} with {top_player.m} matches played."

def get_tournament_by_surface_type(surface=None):
    if not surface:
        return ''

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface
    ).annotate(
        num_matches=Count('matches')
    ).order_by('-start_date')

    if not tournaments.exists():
        return ''

    lines = [
        f'Tournament: {t.name}, start date: {t.start_date}, matches: {t.num_matches}'
        for t in tournaments
    ]
    return '\n'.join(lines)

def get_latest_match_info():
    latest_match = (
        Match.objects
        .select_related('tournament', 'winner')
        .prefetch_related('players')
        .order_by('-date_played', '-id')
        .first()
    )

    if not latest_match:
        return ""


    players = sorted(
        latest_match.players.all(),
        key=lambda p: p.full_name
    )


    players_str = " vs ".join(player.full_name for player in players)

    winner_name = latest_match.winner.full_name if latest_match.winner else "TBA"

    return (
        f"Latest match played on: {latest_match.date_played}, "
        f"tournament: {latest_match.tournament.name}, "
        f"score: {latest_match.score}, "
        f"players: {players_str}, "
        f"winner: {winner_name}, "
        f"summary: {latest_match.summary}"
    )


def get_matches_by_tournament(tournament_name=None):
    if not tournament_name:
        return "No matches found."

    tournament_matches = Match.objects.filter(
        tournament__name__exact=tournament_name
    ).order_by('-date_played')

    if not tournament_matches.exists():
        return "No matches found."

    lines = [
        f'Match played on: {m.date_played}, score: {m.score}, winner: {"TBA" if not m.winner else m.winner.full_name}'
        for m in tournament_matches
    ]

    return '\n'.join(lines)

