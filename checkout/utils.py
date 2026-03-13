from datetime import date

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from memberships.models import UserMembership


def _calculate_membership_end_date(start_date, duration):
    """Calculate membership end date from duration code."""
    if duration == 'quarterly':
        return start_date + relativedelta(months=3)
    if duration == 'annually':
        return start_date + relativedelta(years=1)
    return start_date + relativedelta(months=1)


def activate_membership_for_order(order):
    """Activate/update membership for authenticated user when order contains a membership."""
    if not order.user:
        return False

    membership_item = order.lineitems.select_related('membership').filter(
        membership__isnull=False
    ).first()
    if not membership_item or not membership_item.membership:
        return False

    today = date.today()
    membership_tier = membership_item.membership

    existing = UserMembership.objects.filter(user=order.user).first()
    if (
        existing
        and existing.status == 'active'
        and existing.membership_tier_id == membership_tier.id
        and existing.end_date >= today
    ):
        return True

    UserMembership.objects.update_or_create(
        user=order.user,
        defaults={
            'membership_tier': membership_tier,
            'start_date': today,
            'end_date': _calculate_membership_end_date(today, membership_tier.duration),
            'status': 'active',
            'auto_renew': True,
            'classes_used_this_week': 0,
        },
    )
    return True


def send_order_confirmation_email(order):
    """Send confirmation email for checkout orders (products and/or membership)."""
    has_products = order.lineitems.filter(product__isnull=False).exists()
    has_membership = order.lineitems.filter(membership__isnull=False).exists()
    membership_only = has_membership and not has_products

    membership_item = order.lineitems.select_related('membership').filter(
        membership__isnull=False
    ).first()

    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {
            'order': order,
            'membership_only': membership_only,
            'membership_name': membership_item.membership.name if membership_item and membership_item.membership else '',
        },
    ).strip()

    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {
            'order': order,
            'membership_only': membership_only,
            'membership_name': membership_item.membership.name if membership_item and membership_item.membership else '',
            'contact_email': settings.DEFAULT_FROM_EMAIL,
        },
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )
