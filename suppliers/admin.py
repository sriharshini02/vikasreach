from django.contrib import admin
from .models import (
    Manufacturer,
    Product,
    UserSearchHistory,
    EmailOutreach,
    Ingredient,
    IngredientProduct,
)

admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(UserSearchHistory)
admin.site.register(EmailOutreach)
admin.site.register(Ingredient)
admin.site.register(IngredientProduct)
