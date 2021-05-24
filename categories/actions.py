
from django.utils.translation import ugettext_lazy as _

from categories.models import Category
from cap.actions import related_field_change_action


category_change_action = related_field_change_action(
    Category,
    'category',
    _('Change category')
)
