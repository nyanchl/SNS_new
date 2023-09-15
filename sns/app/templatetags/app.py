from django import template
from django.views.generic import TemplateView

from app.views import BaseView
from app.models import User_config

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter("flag")
def get_negaposi_flag(flag, name):
    print("hoge",flag,name)
    request_user = User_config.objects.get(user=name)
    if flag == True:
        request_user.config = True
        request_user.save()
    else:
        request_user.config = False
        request_user.save()
    
    return None