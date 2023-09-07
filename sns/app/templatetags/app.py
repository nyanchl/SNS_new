from django import template
from django.views.generic import TemplateView

from app.views import BaseView

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)