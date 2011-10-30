"""
Django-sodes models
"""
import os
from datetime import datetime, timedelta

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import slugify
from django.conf import settings

from sodes.util import getters
from sodes.contrib import eyeD3

class Category(models.Model):
    """
    Episode categorization
    
    For use with category/chronology URL confs
    """
    name = models.CharField(max_length=500)
    slug = models.CharField(max_length=500,editable=False,blank=True)
    
    def save(self):
        """
        Custom save, creates slug
        """
        self.slug = slugify(self.name)
        super(Category,self).save()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        """
        Django meta
        """
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    @models.permalink
    def get_absolute_url(self):
        """
        Django permalink
        """
        return ('entry_machine.views.category',[self.slug])

class Sode(models.Model):
    """
    Represents one episode
    """    
    category = models.ForeignKey(Category, null=True, blank=True)
    chronology = models.CharField(max_length=300)
    
    title = models.CharField(max_length=500, help_text="Enter a title for your entry")    
    slug = models.CharField(max_length=500, blank=True, help_text="If left blank, this will be auto generated using your title. <br/>Once saved, this slug will not automatically change if you modify the title.")
    
    image = models.ImageField(null=True, blank=True, help_text="Add an image to the episode, for display on pages", upload_to="global/sodes/images")
    
    blurb = models.TextField(null=True, blank=True, help_text="A short summary or teaser for this entry")
    content = models.TextField(help_text="The full description for this entry")
    
    date = models.DateTimeField(blank=True, help_text="If left blank, this will auto-generate a date for one day from now")
    
    mp3 = models.FileField(upload_to="global/sodes/audio", blank=True, null=True)
    ogg = models.FileField(upload_to="global/sodes/audio", blank=True, null=True)
    
    duration = models.CharField(max_length=30, blank=True, null=True)
    
    def is_published(self):
        return self.date <= datetime.now()
    
    def __unicode__(self):
        return self.title
    
    def _set_date(self):
        """
        If 'date' is not set by user, set it for 1 week in the future
        """
        if not self.date:
            self.date = datetime.now() + timedelta(days=1)  
    
    def _set_slug(self):  
        """
        Creates the slug for the episode
        
        - if the slug is already set, don't auto-generate it
        - if the slug is already taken, append a number
        """
               
        if not self.slug:            
            slug_ok = False 
            current_slug = slugify(self.title)
            append = 0
            
            while not slug_ok:
                try:
                    if self.pk:
                        Sode.objects.get(~Q(pk=self.pk), slug=current_slug)
                    else:
                        Sode.objects.get(slug=current_slug)
                        
                    append = append + 1
                    current_slug = "%s-%s" % (slugify(self.title),append)
                    
                except ObjectDoesNotExist:
                    slug_ok=True
            self.slug = slugify(current_slug)
        
        if self.slug and not self.pk:   
            
            slug_ok = False 
            current_slug = slugify(self.slug)
            append = 0
            
            while not slug_ok:                
                try:                    
                    Sode.objects.get(slug=current_slug)   
                    append = append + 1
                    current_slug = "%s-%s" % (slugify(self.slug),append)
                except ObjectDoesNotExist:
                    slug_ok=True
            self.slug = slugify(current_slug)
    
    class Meta:
        """ Django meta """
        ordering = ['-date']
        get_latest_by = 'date'
        verbose_name_plural = 'Episodes'
        verbose_name = "Episode"
     
    def get_cat_chron(self):
        """
        Return a compiled category / chronology
        """
        return "%s %s" % (self.category, self.chronology)
    get_cat_chron.short_description = "" 
        
    @models.permalink
    def get_absolute_url(self):
        """
        Django permalink
        """
        if getters.use_slugs_for_url():
            return ("sodes.views.single_by_slug", [str(self.slug)])
        else:
            return ("sodes.views.single_by_category", [str(self.category.slug), str(self.chronology)])
        
    def save(self, *args, **kwargs):
        """
        Custom save, auto-generates duration of MP3
        """
        self._set_date()
        self._set_slug()   
        
        super(Sode, self).save(*args, **kwargs)
        
        if not self.duration and self.mp3:
            audio_file = os.path.join(settings.MEDIA_ROOT, str(self.mp3))    
            audiofile = eyeD3.Mp3AudioFile(audio_file)
            self.duration = audiofile.getPlayTimeString()
            super(Sode, self).save(*args, **kwargs)
            
            