
from attributes.models import AttributeValue


def format_attributes(category, entry_ids):

    attrs = []

    attributes = category.attributes.visible()

    values = {attr.id: {} for attr in attributes}

    attr_values_qs = AttributeValue.objects.filter(
        attr__in=attributes,
        entry__in=entry_ids)

    for attr_val in attr_values_qs:
        values[attr_val.attr_id][attr_val.entry_id] = attr_val.as_html()

    for attr in attributes:
        attrs.append({
            'name': attr.name,
            'values': [values[attr.id].get(entry_id) for entry_id in entry_ids]
        })

    return attrs
