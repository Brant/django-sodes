"""
Tags and filters for django-sodes relating to episodes
"""

from django import template

from datetime import datetime
from django.db.models import Avg, Max, Min, Count
from django.template import Template, Context
from django.template.loader import render_to_string
from sodes.models import Sode

from django.utils.datastructures import MultiValueDictKeyError

register = template.Library()

def podcast_archives(context):
    """
    Renders list of archives, by month/year
    """
    episodes = Sode.objects.filter(date__lte=datetime.now()).dates('date', 'month', order='DESC')
    return {'archives': episodes, 'request': context['request']}

register.inclusion_tag('sodes/renders/archive_list.html', takes_context=True)(podcast_archives)


@register.tag("render_podcast")
def do_render_podcast(parser, token):
    """
    Function call for rendering a podcast
    
    {% render_podcast (<variable_name_in_context>) %}
    """
    
    split_token = token.split_contents()
    
    if len(split_token) == 1:
        return RenderPodcastNode()
    
    if not split_token[1] in ["single", "featured", "short"]:
        raise template.TemplateSyntaxError("First argument for %s must be 'single', 'featured', or 'short'" % str(split_token[0]))
    
    render_type = split_token[1]
    var_in_context = "episode"
    render_template = "sodes/renders/single.html"
    extra_context_vars = None
    
    if len(split_token) > 2:
        var_in_context = split_token[2]
        
    if len(split_token) > 3:
        extra_context_vars = split_token[3:]
        
    return RenderPodcastNode(render_type, var_in_context, extra_context_vars)    
    
    
class RenderPodcastNode(template.Node):
    """
    Node for rendering podcasts
    
    short, featured, single
    """
    def __init__(self, render_type="single", var_in_context="episode", extra_context_vars=None):
        """
        Initialize the variable name in the node's context
        """
        self.render_type = render_type
        self.var_in_context = var_in_context
        self.render_template = "sodes/renders/%s.html" % self.render_type
        
        self.extra_context_vars = []
        
        if extra_context_vars:
            for extra_var in extra_context_vars:
                self.extra_context_vars.append(extra_var)
        
    def _build_context_dict(self, context):
        """
        Check for each variable in context, then add it if it exists
        
        Return the dict
        """
        dct = {}
        for item in self.extra_context_vars:
            if item in context:
                dct.update({item: context[item]})
        return dct
        
    def render(self, context):
        """
        Renders the node
        """
        try:
            episode = context[self.var_in_context]
        except KeyError:
            raise template.TemplateSyntaxError("render_single tag recieved no variable in context '%s'" % self.var_in_context)
        
        if not self.var_in_context in context:
            raise template.TemplateSyntaxError("Variable %s not found in context, required for 'render_podcast'" % self.var_in_context)
        
        response_data = self._build_context_dict(context)
        response_data.update({"episode": context[self.var_in_context]})
        
        return render_to_string(self.render_template, response_data)
