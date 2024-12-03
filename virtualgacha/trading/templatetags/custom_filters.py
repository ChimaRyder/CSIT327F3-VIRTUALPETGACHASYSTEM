from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def short_timesince(value):
    if not value:
        return ""

    now_time = timezone.now()
    delta = now_time - value

    days = delta.days
    seconds = delta.seconds

    if days > 365:
        years = days // 365
        return f"{years}y"
    elif days > 30:
        months = days // 30
        return f"{months}m"
    elif days > 0:
        return f"{days}d"
    elif seconds > 3600:
        hours = seconds // 3600
        return f"{hours}h"
    elif seconds > 60:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        return "Just Now"