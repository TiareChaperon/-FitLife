from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def precio_clp(valor):
    try:
        numero = Decimal(str(valor))
        return f"${numero:,.0f}".replace(",", ".")
    except (InvalidOperation, TypeError, ValueError):
        return ""
