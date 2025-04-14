import os
import django
import requests
import re
from dotenv import load_dotenv

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_supply_bot.settings")
django.setup()

from suppliers.models import Manufacturer

# Load .env variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def get_manufacturer_website(manufacturer_name):
    """Fetch the official website of the manufacturer using SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{manufacturer_name} official site",
        "api_key": SERPAPI_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        results = response.json()

        for result in results.get("organic_results", []):
            if (
                "official" in result.get("title", "").lower()
                or "contact" in result.get("title", "").lower()
            ):
                return result.get("link")
    except Exception as e:
        print(f"❌ Error getting website for {manufacturer_name}: {e}")
    return None


def get_contact_details(manufacturer_name):
    """Fetch email and phone number from Google Search using SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{manufacturer_name} contact email phone",
        "api_key": SERPAPI_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        results = response.json()

        emails, phones = set(), set()

        for result in results.get("organic_results", []):
            text = result.get("snippet", "")

            email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
            phone_pattern = (
                r"\+?\d{1,4}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
            )

            emails.update(re.findall(email_pattern, text))
            phones.update(re.findall(phone_pattern, text))

        return {
            "emails": list(emails),
            "phones": list(phones),
        }

    except Exception as e:
        print(f"❌ Error getting contact details for {manufacturer_name}: {e}")
        return {"emails": [], "phones": []}


def update_manufacturer_details():
    manufacturers = (
        Manufacturer.objects.filter(contact_email__isnull=True)
        | Manufacturer.objects.filter(contact_phone__isnull=True)
        | Manufacturer.objects.filter(website__isnull=True)
    )

    for manufacturer in manufacturers:
        print(f"🔍 Checking {manufacturer.name}...")

        # Update website
        if not manufacturer.website:
            website = get_manufacturer_website(manufacturer.name)
            if website:
                manufacturer.website = website
                print(f"🌐 Website updated: {website}")

        # Update email and phone
        if not manufacturer.contact_email or not manufacturer.contact_phone:
            details = get_contact_details(manufacturer.name)
            if details["emails"] and not manufacturer.contact_email:
                manufacturer.contact_email = details["emails"][0]
                print(f"📧 Email updated: {manufacturer.contact_email}")
            if details["phones"] and not manufacturer.contact_phone:
                manufacturer.contact_phone = details["phones"][0]
                print(f"📞 Phone updated: {manufacturer.contact_phone}")

        manufacturer.save()
        print(f"✅ Saved: {manufacturer.name}\n")


if __name__ == "__main__":
    update_manufacturer_details()
