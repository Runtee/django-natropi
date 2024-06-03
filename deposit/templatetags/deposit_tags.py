from django import template
from ..models import Deposit
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def verify_user_deposit(id):
 return format_html('<a href="/deposit/verify/{}" class="verify-link">Verify</a>', id)