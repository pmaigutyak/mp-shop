
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import mail_managers
from django.utils.translation import ugettext_lazy as _


def send_new_size_grid_email(product, sizes):

    subject = '{} #{}'.format(_('New size grid for product'), product.id)

    html = render_to_string('clothes/new_size_grid_email_for_manager.html', {
        'product': product,
        'title': subject,
        'site': Site.objects.get_current(),
        'sizes': sizes
    })

    mail_managers(
        subject=subject,
        message='',
        html_message=html)
