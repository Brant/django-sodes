"""
Paginator stuff for django-sodes index pages
"""

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from sodes.util.getters import get_num_per_page

def make_paginator(request, qs):
    """
    Return a paginated object list
    
    Centralizes how many items per page
    """
    
    paginator = Paginator(qs, get_num_per_page())
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)
    
    return ret