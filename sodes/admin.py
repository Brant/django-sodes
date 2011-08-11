"""
Admin configurations
"""

from django.contrib import admin
from sodes.models import *
from sodes.util import getters
    
class SodeAdmin(admin.ModelAdmin):
    fields = [ "category", "chronology", "title", "date", "blurb", "content", "mp3" ]
    
    if getters.use_ogg():
        fields.append("ogg")
    
    if getters.episode_images():
        fields.insert(2, "image")
        
    if getters.customize_slugs():
        fields.insert(2, "slug")
        
    if getters.show_duration():
        fields.append("duration")
        

admin.site.register(Category)
admin.site.register(Sode, SodeAdmin)