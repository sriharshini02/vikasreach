from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import requests
import time
import random
import os
import django
from .serpapi_fetch import get_manufacturer_contacts

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_supply_bot.settings")
django.setup()

from .models import Manufacturer, Product

# CHROME_DRIVER_PATH = r"C:\\Users\\Public\\SRIHARSHINI\\apps installations\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"


# RapidAPI Credentials
RAPIDAPI_KEY = "4560435427msh81f3effeb7097bep1b5b1bjsn88ef8cb4e42b"
RAPIDAPI_HOST = "real-time-amazon-data.p.rapidapi.com"

# Define Correct Paths
CHROME_BIN = "/opt/render/chrome/chrome-linux64/chrome"
CHROMEDRIVER_BIN = "/opt/render/chromedriver/chromedriver"

# Ensure ChromeDriver has execute permissions
os.chmod(CHROMEDRIVER_BIN, 0o755)

# Configure Chrome Options
chrome_options = Options()
chrome_options.binary_location = CHROME_BIN  # Set custom Chrome binary location
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")


def human_like_delay(min_time=3, max_time=7):
    """Adds a random delay to mimic human behavior and avoid bot detection."""
    time.sleep(random.uniform(min_time, max_time))


def get_manufacturer_selenium(asin, max_retries=3):
    """Scrapes Amazon product page to find manufacturer details using ASIN."""
    url = f"https://www.amazon.com/dp/{asin}?th=1"

    # Start Selenium WebDriver with correct paths
    service = Service(CHROMEDRIVER_BIN)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            human_like_delay()

            # Check for CAPTCHA
            if driver.find_elements(By.ID, "captchacharacters"):
                print(
                    f"⚠ CAPTCHA detected on attempt {retries + 1}. Retrying after delay..."
                )
                time.sleep(random.uniform(10, 15))
                return None

            # Wait for page load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract Manufacturer
            left_cols = soup.find_all("div", class_="a-fixed-left-grid-col a-col-left")
            for left_col in left_cols:
                if "Manufacturer" in left_col.text:
                    right_col = left_col.find_next_sibling(
                        "div", class_="a-fixed-left-grid-col a-col-right"
                    )
                    if right_col:
                        manufacturer_spans = right_col.find_all("span", class_="a-color-base")  # type: ignore
                        manufacturer_data = [
                            span.text.strip()
                            for span in manufacturer_spans
                            if span.text.strip()
                        ]
                        if manufacturer_data:
                            return manufacturer_data[0]

            # If Manufacturer not found, try extracting Brand
            brand_element = soup.find("span", class_="a-size-base po-break-word")
            if brand_element:
                return brand_element.text.strip()

            return None  # Manufacturer not found

        except Exception as e:
            print(f"Error on attempt {retries + 1}: {e}")
            retries += 1
            time.sleep(random.uniform(10, 20))

    print("❌ Max retries reached. Skipping this product.")
    return None


def fetch_manufacturer_details(name):
    """Fetch manufacturer details (website, email, phone) from the database or SerpAPI."""
    manufacturer = Manufacturer.objects.filter(name__iexact=name).first()

    if manufacturer:
        return {
            "name": manufacturer.name,
            "website": manufacturer.website,
            "contact_email": manufacturer.contact_email,
            "contact_phone": manufacturer.contact_phone,
        }
    manufacturer_data = get_manufacturer_contacts(name)

    if manufacturer_data:
        manufacturer = Manufacturer.objects.create(
            name=name,
            website=manufacturer_data["website"],
            contact_email=(
                manufacturer_data["emails"][0] if manufacturer_data["emails"] else None
            ),
            contact_phone=(
                manufacturer_data["phones"][0] if manufacturer_data["phones"] else None
            ),
        )
        return {
            "name": manufacturer.name,
            "website": manufacturer.website,
            "contact_email": manufacturer.contact_email,
            "contact_phone": manufacturer.contact_phone,
        }

    return None


def scrape_products(search_query):
    """Scrapes Amazon for product details using raw material search queries."""
    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    querystring = {
        "query": search_query,
        "page": "1",
        "country": "US",
        "sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE",
    }

    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}

    response = requests.get(url, headers=headers, params=querystring)

    try:
        response_json = response.json()
    except json.JSONDecodeError:
        print("❌ Failed to decode JSON response.")
        return []

    if "data" not in response_json or "products" not in response_json["data"]:
        print("❌ No product data found.")
        return []

    products = response_json["data"]["products"]
    product_list = []
    ind = 0
    for product in products:
        asin = product["asin"]
        title = product["product_title"]
        manufacturer_name = get_manufacturer_selenium(asin)

        # Fetch manufacturer details from DB
        manufacturer_details = (
            fetch_manufacturer_details(manufacturer_name) if manufacturer_name else None
        )

        # Store new manufacturer if not in database
        manufacturer = None
        if manufacturer_details:
            manufacturer, created = Manufacturer.objects.get_or_create(
                name=manufacturer_details["name"],
                defaults={
                    "website": manufacturer_details["website"],
                    "contact_email": manufacturer_details["contact_email"],
                    "contact_phone": manufacturer_details["contact_phone"],
                },
            )
        else:
            if manufacturer_name:
                manufacturer, created = Manufacturer.objects.get_or_create(
                    name=manufacturer_name
                )

        # Save product
        product_obj, created = Product.objects.get_or_create(
            name=title,
            defaults={
                "category": None,
                "website": None,
                "raw_materials": search_query,
                "manufacturer": manufacturer,
            },
        )

        product_list.append(
            {
                "ASIN": asin,
                "Title": title,
                "Manufacturer": (
                    manufacturer_details
                    if manufacturer_details
                    else {
                        "name": manufacturer_name,
                        "website": None,
                        "contact_email": None,
                        "contact_phone": None,
                    }
                ),
            }
        )
        ind += 1
        if ind == 5:
            break
        human_like_delay(3, 8)

    return product_list
