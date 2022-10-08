from django.http import HttpResponse

class StripeWH_Handler:
    """ 
    Handle Stripe webhooks
    I borrowed this code from code institute, from the project
    boutique Ado
    """
    
    def __init__(self, request):
        self.request = request

    
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
        print(intent)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ Handle payment_intent.payment_failed webhook from stripe
            I borrowed this code from code institute, from the project
            boutique Ado"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
        