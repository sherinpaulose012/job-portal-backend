from django.contrib import admin
from .models import (
    SubscriptionPlan,
    UserSubscription,
    PaymentTransaction,
    BillingHistory,
)

admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(PaymentTransaction)
admin.site.register(BillingHistory)