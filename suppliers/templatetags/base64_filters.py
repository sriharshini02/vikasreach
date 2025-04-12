# suppliers/templatetags/base64_filters.py
import base64
from django import template

register = template.Library()


@register.filter
def base64_id(value):
    """Converts email (or any string) to a safe HTML id using base64."""
    if not value:
        return "unknown"
    return base64.urlsafe_b64encode(value.encode()).decode("utf-8").rstrip("=")
