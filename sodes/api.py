"""
Some simple API stuff
"""
from datetime import datetime
from sodes.models import Sode

def get_latest_episodes(count=5):
    """
    Return the latest, published episodes
    """
    return Sode.objects.filter(date__lte=datetime.now(), mp3__isnull=False)[:count]
    