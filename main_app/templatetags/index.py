from django.template import Library
register = Library()
from ..static_data.lookups import indexed_variables, inverse_names

# Adding custom template tags to enable accessing values in dicts by index
@register.filter
def get_variable_by_index(index):
    for key, value in indexed_variables.items():
        if value == index:
            return key
    return None

@register.filter
def get_inverse_name(key):
    return inverse_names.get(key, key)
