
from django.utils.translation import ugettext_lazy as _


ATTR_TYPE_TEXT = 1
ATTR_TYPE_INT = 2
ATTR_TYPE_BOOL = 3
ATTR_TYPE_SELECT = 5

ATTR_TYPES = (
    (ATTR_TYPE_TEXT, _("Text")),
    (ATTR_TYPE_INT, _("Integer")),
    (ATTR_TYPE_BOOL, _("True / False")),
    (ATTR_TYPE_SELECT, _("Options")),
)
