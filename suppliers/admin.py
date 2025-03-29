from django.contrib import admin
from .models import Manufacturer, Product, UserSearchHistory, EmailOutreach

admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(UserSearchHistory)
admin.site.register(EmailOutreach)
