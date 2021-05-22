
import django.dispatch

manufacturer_replaced = django.dispatch.Signal(
    providing_args=['src_id', 'dst_id'])
