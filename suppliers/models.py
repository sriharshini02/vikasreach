from django.contrib.auth.models import User
from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    website = models.URLField(blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)  # optional
    ingredients = models.ManyToManyField(
        "Ingredient", through="IngredientProduct", related_name="products"
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class IngredientProduct(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ingredient.name} in {self.product.name}"


class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.search_query}"


class EmailOutreach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    email_subject = models.CharField(max_length=255)
    email_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "manufacturer")  # Ensure no duplicates

    def __str__(self):
        return f"Email to {self.manufacturer.name} by {self.user.username}"
