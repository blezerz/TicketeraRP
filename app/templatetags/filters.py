from django import template
import os

register = template.Library()

@register.filter
def basename(value):
    """
    Retorna el nombre base del archivo (sin la ruta).
    """
    return os.path.basename(value)
