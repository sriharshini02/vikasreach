from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage
from collections import defaultdict
from .models import Ingredient, IngredientProduct


@login_required
def home(request):
    manufacturers_by_product = defaultdict(list)
    query = ""

    if request.method == "POST":
        if "query" in request.POST:
            query = request.POST.get("query", "").strip().lower()

            if query:
                try:
                    ingredient = Ingredient.objects.get(name__iexact=query)
                    product_links = IngredientProduct.objects.filter(
                        ingredient=ingredient
                    )
                    product_ids = product_links.values_list("product_id", flat=True)
                    products = Product.objects.filter(id__in=product_ids)

                    # Track unique manufacturers by name + email
                    seen = set()

                    for product in products:
                        manufacturer = product.manufacturer
                        if manufacturer:
                            identifier = (manufacturer.name, manufacturer.contact_email)
                            if identifier not in seen:
                                seen.add(identifier)
                                manufacturers_by_product[product.category].append(
                                    {
                                        "name": manufacturer.name,
                                        "website": manufacturer.website or "#",
                                        "contact_email": manufacturer.contact_email
                                        or "Not Available",
                                        "contact_phone": manufacturer.contact_phone
                                        or "Not Available",
                                    }
                                )

                except Ingredient.DoesNotExist:
                    # If no matching ingredient found, show nothing
                    pass

        elif "manufacturer_email" in request.POST:
            manufacturer_email = request.POST.get("manufacturer_email")
            manufacturer_name = request.POST.get("manufacturer_name")
            user_email = request.user.email

            if not manufacturer_email or manufacturer_email == "Not Available":
                return JsonResponse(
                    {
                        "success": False,
                        "message": "No email available for this manufacturer.",
                    }
                )

            subject = f"Business Inquiry Regarding {manufacturer_name}"
            message = f"""
            Dear {manufacturer_name},

            I am reaching out as I am interested in collaborating with your company. 
            I would love to discuss potential business opportunities with you. 

            Please let me know a convenient time to connect.

            Best Regards,  
            {request.user.username}  
            {user_email}
            """

            try:
                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [manufacturer_email],
                    bcc=[user_email],
                    reply_to=[user_email],
                )
                email.send()

                return JsonResponse(
                    {"success": True, "message": "Email sent successfully!"}
                )
            except Exception as e:
                return JsonResponse(
                    {"success": False, "message": f"Error sending email: {str(e)}"}
                )

    return render(
        request,
        "home.html",
        {"manufacturers_by_product": dict(manufacturers_by_product), "query": query},
    )


from django.http import JsonResponse


@login_required
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        title = request.POST.get("title")
        message = request.POST.get("message")

        full_message = f"From: {name} ({email})\n\n{message}"

        send_mail(
            subject=title,
            message=full_message,
            from_email=email,
            recipient_list=["vikasreach02@gmail.com"],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")

    return render(request, "contact.html")


def about_view(request):
    return render(request, "about.html")
