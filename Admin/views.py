from django.shortcuts import render
from Home.models import Subscription_nowcook
from django.utils import timezone
# Create your views here.
def admin_daily_order_summary(request):
    today = timezone.now().date()

    # Initialize counters
    orders = {
        'lunch': {'Basic': 0, 'Premium': 0},
        'dinner': {'Basic': 0, 'Premium': 0}
    }

    # Get all subscriptions active today
    subscriptions = Subscription_nowcook.objects.filter(start_date__lte=today, end_date__gte=today)
    information=Subscription_nowcook.objects.filter(user=request.user)

    # Calculate orders
    for subscription in subscriptions:
        if subscription.category == 'Regular':
            if not subscription.is_lunch_off:
                orders['lunch']['Basic'] += 1
            if not subscription.is_dinner_off:
                orders['dinner']['Basic'] += 1
        elif subscription.category == 'Premium':
            if not subscription.is_lunch_off:
                orders['lunch']['Premium'] += 1
            if not subscription.is_dinner_off:
                orders['dinner']['Premium'] += 1

    context = {
        'orders': orders,
        'today': today,
        'info':information,
    }

    return render(request, 'admin_daily_order_summary.html', context)