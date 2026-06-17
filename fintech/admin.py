from django.contrib import admin

from .models import (
    Account,
    Merchant,
    Card,
    Transaction
)

admin.site.register(Account)
admin.site.register(Merchant)
admin.site.register(Card)
admin.site.register(Transaction)