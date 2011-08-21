"""
Views for django-sodes
"""

from datetime import datetime, date

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from sodes.models import Sode, Category
from sodes.util.paginator import make_paginator
from sodes.util.getters import use_paginator, use_slugs_for_url

from django.http import Http404

def archive(request, year, month, template_name="sodes/archive.html"):
    """
    List of published episodes, by year/month
    """
    episodes = Sode.objects.filter(
        date__lte=datetime.now(),
        date__year=year,
        date__month=month,
        mp3__isnull=False
    )
    
    if use_paginator():
        episodes = make_paginator(request, episodes)
    
    return render_to_response(template_name, {
            'episodes': episodes,
            'archive_date': date(int(year), int(month), 1)
        },
        context_instance=RequestContext(request)
    )


def index(request, template_name="sodes/index.html"):
    """ 
    Published episode list
    """
    episodes = Sode.objects.filter(date__lte=datetime.now(), mp3__isnull=False)
    
    if use_paginator():
        episodes = make_paginator(request, episodes)
    
    return render_to_response(template_name, {"episodes": episodes}, context_instance=RequestContext(request))

def single_by_category(request, category, chronology, template_name="sodes/single.html"):
    """
    Single episode, uses category/chronology based URL conf
    
    Superusers can view unpublished episodes
    """
    if request.user.is_superuser:
        episode = get_object_or_404(Sode, category__slug=category, chronology=chronology, mp3__isnull=False)
    else:
        episode = get_object_or_404(Sode, category__slug=category, chronology=chronology, mp3__isnull=False, date__lte=datetime.now())
        
    return render_to_response(template_name, {"episode": episode}, context_instance=RequestContext(request))

def single_by_slug(request, slug, template_name="sodes/single.html"):
    """
    Single episode, uses slug-based URL conf
    
    Superusers can view unpublished episodes
    """
    if request.user.is_superuser:
        episode = get_object_or_404(Sode, slug=slug, mp3__isnull=False)
    else:
        episode = get_object_or_404(Sode, slug=slug, mp3__isnull=False, date__lte=datetime.now())
        
    return render_to_response(template_name, {"episode": episode}, context_instance=RequestContext(request))