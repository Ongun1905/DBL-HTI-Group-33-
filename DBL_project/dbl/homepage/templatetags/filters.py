# This file registers filters: Functions that can be applied onto variables in Django template files in order to manipulate the form of the data.
from django import template

register = template.Library()

# Filter for selecting an element in a list by the index of a for loop
@register.filter
def index(sequence, position):
    return sequence[position]
