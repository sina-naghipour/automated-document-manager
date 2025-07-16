from django import template
import re

register = template.Library()

@register.filter
def filename(value):
    return re.sub(r'^.*/([^/]+)$', r'\1', value)