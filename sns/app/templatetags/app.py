from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # print("dictionary:",dictionary,",key:",key)
    return dictionary.get(key)