from django import template

register = template.Library()

# Allows Django template to use dynamic keys
@register.filter
def getvalue(dictionary, key):
    return dictionary.get(key)
