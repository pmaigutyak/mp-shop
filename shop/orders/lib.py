
from django.apps import apps
from django.conf import settings
from django.core.mail import mail_managers, send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


def send_new_order_notifications(order):

    from django.contrib.sites.models import Site

    subject = _('New order #%s') % order.id

    context = {'order': order, 'site': Site.objects.get_current()}

    email_template_name = 'orders/email/new_order_notification_for_admins.html'

    html = render_to_string(email_template_name, context)

    mail_managers(subject=subject, message='', html_message=html)

    if apps.is_installed('turbosms'):

        from turbosms.lib import send_sms_from_template

        sms_template_name = 'orders/sms/new_order_notification_for_admins.txt'

        send_sms_from_template(sms_template_name, context)

    if order.email:

        email_template_name = (
            'orders/email/new_order_notification_for_customer.html')

        html = render_to_string(email_template_name, context)

        send_mail(subject, '', settings.EMAIL_HOST_USER, [order.email],
                  html_message=html)
