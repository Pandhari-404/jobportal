"""
jobs/templatetags/job_tags.py
==============================
Custom template tags and filters for the JobSpark portal.

Usage in templates:
    {% load job_tags %}
    {{ job.pk|is_in_set:saved_ids }}
    {{ value|subtract:other }}
"""

from django import template

register = template.Library()


@register.filter(name='is_in_set')
def is_in_set(value, the_set):
    """Return True if value is in the given set/list."""
    return value in the_set


@register.filter(name='subtract')
def subtract(value, arg):
    """Subtract arg from value."""
    try:
        return int(value) - int(arg)
    except (TypeError, ValueError):
        return value


@register.simple_tag(takes_context=True)
def active_if(context, url_name):
    """Return 'active' CSS class if current URL matches url_name."""
    request = context.get('request')
    if request and request.resolver_match.url_name == url_name:
        return 'active'
    return ''


@register.filter(name='first_char')
def first_char(value):
    """Return the first character of a string, uppercased."""
    if value:
        return str(value)[0].upper()
    return '?'
