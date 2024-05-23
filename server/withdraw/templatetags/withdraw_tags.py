from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def verify_user_withdraw(id):
 return format_html('<a href="/withdraw/verify/{}" class="verify-link">Verify</a>', id)