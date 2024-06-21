import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(TemplateView):
    template_name = 'premium/premium.html'

@login_required
def create_checkout_session(request, pk):
    price_id = 'price_1PTWJHHnlYC0Y6TE1YfJhG66'
    user = request.user

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment:success')),
        cancel_url=request.build_absolute_uri(reverse('payment:cancel')),
    )

    user.is_premium = True
    user.save()

    return redirect(session.url, code=303)

@method_decorator(login_required, name='dispatch')
class SuccessView(TemplateView):
    template_name = 'premium/premium.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_premium:
            messages.error(request, 'Sorry. You are not authorized to view this page.')
            return redirect("payment:home")

        messages.success(request, 'Thank you. Your payment was successfully processed and your premium status is now active!')

        return redirect("payment:home")

class CancelView(TemplateView):
    template_name = 'premium/premium.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_premium:
            messages.error(request, 'Sorry. You are not authorized to view this page.')
            return redirect("payment:home")

        messages.error(request, 'Sorry. Your payment was canceled!')
        return redirect("payment:home")
