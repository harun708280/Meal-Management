from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from autoslug import AutoSlugField
class Plan(models.Model):
    item = models.IntegerField()
    Reguler_balance = models.IntegerField(null=True)
    Primium_balance = models.IntegerField(null=True)
    p_slug=AutoSlugField(populate_from='item', unique=True, null=True)

    def __str__(self):
        return str(self.item)  

class Subscription_nowcook(models.Model):
    PLAN_CHOICES = [
        (3, '3 Days'),
        (7, '7 Days'),
        (15, '15 Days'),
        (30, '30 Days'),
    ]
    CATEGORY_CHOICES = [
        ('Regular', 'Regular'),
        ('Premium', 'Premium'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    plan = models.IntegerField(choices=PLAN_CHOICES, blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    is_lunch_off = models.BooleanField(default=False)
    is_dinner_off = models.BooleanField(default=False)
    Reguler_balance = models.ForeignKey(Plan, related_name='regular_subscriptions', on_delete=models.CASCADE, null=True)
    Primium_balance = models.ForeignKey(Plan, related_name='premium_subscriptions', on_delete=models.CASCADE, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True) 
    # other relevant fields
    
    def line_Total(self):
        return self.Reguler_balance.Reguler_balance * self.plan if self.category == 'Regular' else 0
    
    def pri_line(self):
        return self.Primium_balance.Primium_balance * self.plan if self.category == 'Premium' else 0
    
    

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = datetime.now().date()
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan)
        if not self.Reguler_balance:
            # Fetch a default Plan instance for Regular if not provided
            default_regular_plan = Plan.objects.filter(item=self.plan).first()
            if default_regular_plan:
                self.Reguler_balance = default_regular_plan
        if not self.Primium_balance:
            # Fetch a default Plan instance for Premium if not provided
            default_premium_plan = Plan.objects.filter(item=self.plan).first()
            if default_premium_plan:
                self.Primium_balance = default_premium_plan
        super().save(*args, **kwargs)

    def consume_meal(self, meal_type):
        if meal_type == 'lunch' and not self.is_lunch_off:
            if self.category == 'Regular' and self.Reguler_balance.Reguler_balance > 0:
                self.Reguler_balance.Reguler_balance -= 1
            elif self.category == 'Premium' and self.Primium_balance.Primium_balance > 0:
                self.Primium_balance.Primium_balance -= 1
        elif meal_type == 'dinner' and not self.is_dinner_off:
            if self.category == 'Regular' and self.Reguler_balance.Reguler_balance > 0:
                self.Reguler_balance.Reguler_balance -= 1
            elif self.category == 'Premium' and self.Primium_balance.Primium_balance > 0:
                self.Primium_balance.Primium_balance -= 1
        self.save()
