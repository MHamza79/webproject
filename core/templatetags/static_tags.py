from django import template
from django.contrib.staticfiles.finders import find
register = template.Library()

@register.filter
def static_exists(static_path):
    return find(static_path) is not None
