import os
import django
from django.db.models import Count
# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match
# Create queries within functions


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ''

    if search_name is not None and search_country is not None:
        players = TennisPlayer.objects.filter(
            full_name__icontains=search_name, country__icontains=search_country).order_by('ranking')
    elif search_name is not None:
        players = TennisPlayer.objects.filter(full_name__icontains=search_name).order_by('ranking')
    else:
        players = TennisPlayer.objects.filter(country__icontains=search_country).order_by('ranking')

    players_info = []
    for player in players:
        players_info.append(
            f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")
    return '\n'.join(players_info) if players_info else ''


def get_top_tennis_player():
    top_players = TennisPlayer.objects.get_tennis_players_by_wins_count()
    if top_players:
        top_player = top_players.first()
        return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."
    return ""


def get_tennis_player_by_matches_count():
    player = (TennisPlayer.objects.annotate(matches_count=Count('match'))
              .order_by('-matches_count', 'ranking')
              .first())

    if not player or player.matches_count == 0:
        return ''

    return f"Tennis Player: {player.full_name} with {player.matches_count} matches played."


def get_tournaments_by_surface_type(surface=None):
    if surface is None:
        return ""
    tournaments = (Tournament.objects.prefetch_related('match_set').annotate(num_matches=Count('match'))
                   .filter(surface_type__icontains=surface).order_by('-start_date'))
#   tournaments = Tournament.objects.filter(
#       surface_type__icontains=surface).annotate(num_matches=Count('match')).order_by('-start_date')

    if not tournaments.exists():
        return ""

    result = []
    for tournament in tournaments:
        result.append(f"Tournament: {tournament.name}, start date: {tournament.start_date}, matches: {tournament.num_matches}")
    return "\n".join(result)


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()
    # latest_match = Match.objects.order_by('-date_played', '-id').first()
    if not latest_match:
        return ""

    players = latest_match.players.order_by('full_name')
    players_str = " vs ".join(player.full_name for player in players)
    winner_str = latest_match.winner.full_name if latest_match.winner else "TBA"

    return (f"Latest match played on: {latest_match.date_played}, tournament: {latest_match.tournament.name}, "
            f"score: {latest_match.score}, players: {players_str}, winner: {winner_str}, summary: {latest_match.summary}")


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    # matches = Match.objects.filter(tournament__name=tournament_name).order_by('-date_played')
    matches = (Match.objects.select_related('tournament', 'winner')
               .filter(tournament__name=tournament_name).order_by('-date_played'))
    if not matches.exists():
        return "No matches found."

    result = []
    for match in matches:
        winner_str = match.winner.full_name if match.winner else "TBA"
        result.append(f"Match played on: {match.date_played}, score: {match.score}, winner: {winner_str}")
    return "\n".join(result)
