
from django.apps import apps
from django.core.mail import mail_managers
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


def send_new_price_offer_notification(offer):

    subject = _('New product price offer #%s') % offer.id

    current_site = Site.objects.get_current()

    context = {'offer': offer, 'site': current_site}

    html = render_to_string('offers/notifications/email.html', context)

    mail_managers(subject=subject, message='', html_message=html)

    if apps.is_installed('turbosms'):

        from turbosms.lib import send_sms_from_template

        send_sms_from_template('offers/notifications/sms.txt', context)
