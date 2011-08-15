"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test.client import Client
from django.test import TestCase
from django.conf import settings

from sodes.models import Sode
from sodes.templatetags import sode_tags as tags
from sodes.util import getters

class URLConfTestCase(TestCase):
    """
    Test our "settingified" urls
    """
    fixtures = ["sodes_tests.json"]
    urls = "sodes.urls"
    
    def setUp(self):
        """
        Set some stuff up, Grab some data
        """
        self.sode = Sode.objects.get(pk=1)
        self.client = Client()
    
        base_url = reverse("sodes.views.index")
        self.cat_url = "%s%s/%s/" % (base_url, self.sode.category.slug, self.sode.chronology)
        self.slug_url = "%s%s/" % (base_url, self.sode.slug)
        
    def test_urls_no_reverse(self):
        """
        URL conf for single sode should change based on settings
        """
        if getters.use_slugs_for_url():
            with self.assertRaises(NoReverseMatch):
                reverse("sodes.views.single_by_category", kwargs={"category": self.sode.category.slug, "chronology": self.sode.chronology})
            reverse("sodes.views.single_by_slug", kwargs={"slug": self.sode.slug})
        else:
            with self.assertRaises(NoReverseMatch):
                reverse("sodes.views.single_by_slug", kwargs={"slug": self.sode.slug})
            reverse("sodes.views.single_by_category", kwargs={"category": self.sode.category.slug, "chronology": self.sode.chronology})
    
    def test_urls_404(self):
        """
        Test correct 404s based on settings
        """        
        base_url = reverse("sodes.views.index")
        cat_url = "%s%s/%s/" % (base_url, self.sode.category.slug, self.sode.chronology)
        slug_url = "%s%s/" % (base_url, self.sode.slug)
        
        if getters.use_slugs_for_url():    
            response = self.client.get(slug_url)
            self.assertEquals(response.status_code, 200)
            response = self.client.get(cat_url)
            self.assertEquals(response.status_code, 404)
        else:
            response = self.client.get(slug_url)
            self.assertEquals(response.status_code, 404)
            response = self.client.get(cat_url)
            self.assertEquals(response.status_code, 200)
            

class ModelsTestCase(TestCase):
    """
    Tests relating to models
    """
    def test_save(self):
        """
        On saves, if there is a slug defined, it should not get overwritten
        """
        sode = Sode(title="YoYo")
        sode.save()
        self.assertEquals(sode.slug, "yoyo")
        
        sode = Sode(title="YoYo", slug="heyo")
        sode.save()
        self.assertEquals(sode.slug, "heyo")
    

class RenderPodcastTestCase(TestCase):
    """
    {% render_podcast %} template tag
    """
    def test_render_defaults(self):
        """
        defaults:
            render_type: single
            var_in_context: episode
            render_template: sodes/renders/<render_type>.html
        """
        node = tags.RenderPodcastNode()
        self.assertEquals("single", node.render_type)
        self.assertEquals("episode", node.var_in_context)
        self.assertEquals("sodes/renders/single.html", node.render_template)
    
    def test_init(self):
        """
        Test setting some stuff that isnt defaults
        """
        node = tags.RenderPodcastNode("asdf", "yoyo")
        self.assertEquals("asdf", node.render_type)
        self.assertEquals("yoyo", node.var_in_context)
        self.assertEquals("sodes/renders/asdf.html", node.render_template)
    
    def test_template_switch(self):
        """
        changing the render type shoudl also change the render_template
        """
        node = tags.RenderPodcastNode("asdf")
        self.assertEquals("asdf", node.render_type)
        self.assertEquals("sodes/renders/asdf.html", node.render_template)
        
    
        