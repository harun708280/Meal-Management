from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, time
import pytz
from.models import*

def home(request):
    all=Plan.objects.all()
    return render(request,'home.html',locals())

def subscribe(request,slug):
    new=Plan.objects.get(p_slug=slug)
    if request.method == 'POST':
        
        category = request.POST.get('category')
        plan = int(request.POST.get('plan'))  

        
        start_date = timezone.now().date()
        end_date = start_date + timezone.timedelta(days=plan)

        
        subscription = Subscription_nowcook.objects.create(
            user=request.user,  
            category=category,
            plan=plan,
            
        )
        subscription.save

        
        return redirect('dashboard')

    return render(request, 'subscribe.html',locals())

def toggle_meal_off(request, meal_type):
    user = request.user
    try:
        subscriptions = Subscription_nowcook.objects.filter(user=user)
    except ObjectDoesNotExist:
        return redirect('subscription_page')

    
    dhaka_timezone = pytz.timezone('Asia/Dhaka')
    current_time = datetime.now(dhaka_timezone).time()
    print( {current_time})

    for subscription in subscriptions:
        if meal_type == 'lunch':
           
            if time(0, 0) <= current_time < time(9, 0):
                print("Toggling lunch")
                subscription.is_lunch_off = not subscription.is_lunch_off
        elif meal_type == 'dinner':
            
            if time(12, 0) <= current_time < time(18, 0):
                print("Toggling dinner")
                subscription.is_dinner_off = not subscription.is_dinner_off
        elif meal_type == 'both':
           
            if (time(0, 0) <= current_time < time(23, 0)):
                print("Toggling both lunch and dinner")
                subscription.is_lunch_off = not subscription.is_lunch_off
                subscription.is_dinner_off = not subscription.is_dinner_off
        subscription.save()

    return redirect('dashboard')

def meal_off_view(request):
    if request.method == 'POST':
        meal_type = request.POST.get('meal_type')
        if meal_type in ['lunch', 'dinner', 'both']:
            return toggle_meal_off(request, meal_type)
    return render(request, 'meal_off.html')

def dashboard(request):
    user_subscriptions = Subscription_nowcook.objects.filter(user=request.user)
    context = {
        'user_subscriptions': user_subscriptions,
    }
    return render(request, 'dashboards.html', context)

