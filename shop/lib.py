
import re

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail


def round_number(value, decimal_places=2, down=False):

    assert decimal_places > 0
    factor = 1.0 ** decimal_places
    sign = -1 if value < 0 else 1
    return int(value * factor + sign * (0 if down else 0.5)) / factor


def format_number(value):

    append_comma = lambda match_object: "%s," % match_object.group(0)

    value = "%.2f" % float(value)
    value = re.sub("(\d)(?=(\d{3})+\.)", append_comma, value)

    return value


def format_price(price, round_price=False):
    price = float(price)
    return format_number(round_number(price) if round_price else price)


def get_show_on_site_link(url):
    return mark_safe(
        '<a href="%s" target="_blank">%s</a>' % (url, _('Show on site')))


def get_preview(field, width=100):

    if not field:
        return '-----'
    try:
        url = get_thumbnail(field.file, str(width)).url
    except IOError:
        return _('Image not found')

    return mark_safe('<img src="%s" style="width: %spx;" title="%s" />' % (
        url, width, field.path))
