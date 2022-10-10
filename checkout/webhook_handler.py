import json
import time
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from userprofiles.models import CustomerProfile

from items.models import Item

from .models import Ordering, OrderingLineItem


class StripeWH_Handler:
    """ 
    Handle Stripe webhooks
    I borrowed this code from code institute, from the project
    boutique Ado
    """
    
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, ordering):
        """
        Send the customer a confirmation email
        """
        cust_email = ordering.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'ordering': ordering}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'ordering': ordering, 'lasershop_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )
    
    def handle_event(self, event):
        """ 
        Handle a generic/unknown/unexpected webhook event
        I borrowed this code from code institute, from the project
        boutique Ado
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook from stripe
        I borrowed this code from code institute, from the project
        boutique Ado
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        sum_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        # Update customer information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = CustomerProfile.objects.get(user__username=username)
            if save_info:
                profile.default_mobile_number = shipping_details.phone,
                profile.default_zip_code = shipping_details.address.postal_code,
                profile.default_street_address = shipping_details.address.line1,
                profile.default_city = shipping_details.address.city,
                profile.default_country = shipping_details.address.country
                profile.save()


        ordering_exists = False
        attempt = 1
        while attempt <= 4:

            try:

                ordering = Ordering.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    mobile_number__iexact=shipping_details.phone,
                    zip_code__iexact=shipping_details.address.postal_code,
                    street_address__iexact=shipping_details.address.line1,
                    city__iexact=shipping_details.address.city,
                    country__iexact=shipping_details.address.country,
                    sum_total=sum_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                ordering_exists = True
                break
            
            except Ordering.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if ordering_exists:
            self._send_confirmation_email(ordering)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | \
                    SUCCESS: Verified order already in database',
                status=200)

        else:
            ordering = None

            try:
                ordering = Ordering.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    mobile_number=shipping_details.phone,
                    zip_code=shipping_details.address.postal_code,
                    street_address=shipping_details.address.line1,
                    city=shipping_details.address.city,
                    country=shipping_details.address.country,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, values in json.loads(bag).items():
                    item = get_object_or_404(Item, pk=values['id'])
                    ordering_line_item = OrderingLineItem(
                        ordering=ordering,
                        item=item,
                        amount=values.get('amount'),
                        name_engraved=values.get('name')
                        
                    )
                    ordering_line_item.save()
            except Exception as e:
                if ordering:
                    ordering.delete()
                return HttpResponse(
                    content=f'Webhook received:{event["type"]} | \
                         ERROR: {e}',
                    status=500)
        self._send_confirmation_email(ordering)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
                 SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle payment_intent.payment_failed webhook from stripe
            I borrowed this code from code institute, from the project
            boutique Ado"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
        