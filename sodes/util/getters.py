"""
Default/settings selection for various important variables

Each checks for a user-defined variable first, the defaults to whatever is set in util.defaults
"""
from django.conf import settings
from sodes.util import defaults

def use_slugs_for_url():
    """
    Which URL schemes are we using?
    
    Default is to use category/chronology schemes
    """
    try:
        return settings.SODES_SLUG_URLS
    except AttributeError:
        return defaults.SODES_SLUG_URLS
    
def use_paginator():
    """
    Is pagination enabled?
    """
    try:
        return settings.SODES_USE_PAGINATOR
    except AttributeError:
        return defaults.SODES_USE_PAGINATOR
    
def get_num_per_page():
    """
    How many items per page are we set to show?
    """
    try:
        return settings.SODES_PER_PAGE
    except AttributeError:
        return defaults.SODES_PER_PAGE
    
def use_ogg():
    """
    Are we uploading OGG's as well as MP3?
    """
    try:
        return settings.SODES_USE_OGG
    except AttributeError:
        return defaults.SODES_USE_OGG
    
def customize_slugs():
    """
    Are we allowing customized slugs (or just auto generated) ?
    """
    try:
        return settings.SODES_CUSTOM_SLUGS
    except AttributeError:
        return defaults.SODES_CUSTOM_SLUGS
    
def episode_images():
    """
    Are we allowing the addition of a "thumbnail" for each episode?
    """
    try:
        return settings.SODES_USE_IMAGES
    except AttributeError:
        return defaults.SODES_USE_IMAGES
    
def show_duration():
    """
    Show the duration in the admin panel?
    """
    try:
        return settings.SODES_SHOW_DURATION
    except AttributeError:
        return defaults.SODES_SHOW_DURATION
    