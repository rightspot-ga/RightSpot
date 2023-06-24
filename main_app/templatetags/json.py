from django import template
from django.utils.html import escapejs
import json

register = template.Library()

@register.filter(is_safe=True)
def escapejs_json(data):
    return escapejs(json.dumps(data))