from django import template
from orders.models import Order

register = template.Library()

@register.filter
def get_status_color(value):
    status_colors = {
        'pending': 'yellow',
        'processing': 'orange',
        'shipped': 'blue',
        'delivered': 'grey',
        'cancelled': 'red',
    }
    return status_colors.get(value, 'green')
