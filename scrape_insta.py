from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, unquote
import time
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_supply_bot.settings")
django.setup()

from suppliers.models import Product, Manufacturer, Ingredient, IngredientProduct
from suppliers.serpapi_fetch import get_manufacturer_contacts

# Setup Selenium
options = Options()
# options.add_argument('--headless')  # Uncomment for headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

search_term = "chips"
url = f"https://www.instacart.com/store/s?k={search_term}"
driver.get(url)
time.sleep(15)

# Scroll to load all products
prev_count = 0
repeats = 0
max_repeats = 5

while True:
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(7)
    items = driver.find_elements(
        By.CSS_SELECTOR, "li[data-testid='CrossRetailerResultRowWrapper']"
    )
    curr_count = len(items)
    print(f"Items loaded: {curr_count}")
    if curr_count == prev_count:
        repeats += 1
    else:
        repeats = 0
    if repeats >= max_repeats:
        break
    prev_count = curr_count

# Extract product links
print("\nExtracting product links...")
product_links = set()
for li in items:
    anchors = li.find_elements(By.TAG_NAME, "a")
    for a in anchors:
        href = a.get_attribute("href")
        if href and "/products/" in href:
            if not href.startswith("http"):
                href = "https://www.instacart.com" + href
            product_links.add(href)

print(f"\n✅ Found {len(product_links)} product links.")

# Visit each product and store info
for url in product_links:
    driver.get(url)
    time.sleep(5)

    # Extract product name from URL slug
    product_slug = urlparse(url).path.split("/")[-1]
    product_name = unquote(product_slug).replace("-", " ").title()

    # Manufacturer name
    try:
        manufacturer_name = driver.find_element(By.CLASS_NAME, "e-10iahqc").text.strip()
    except:
        manufacturer_name = None

    # Scroll to bottom to get ingredients
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    try:
        ingredients_h2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Ingredients']"))
        )
        ingredients_p = ingredients_h2.find_element(
            By.XPATH, "following-sibling::div/p"
        )
        ingredients_raw = ingredients_p.text.strip().split(".")[0]
        ingredients_list = [i.strip() for i in ingredients_raw.split(",")]
    except:
        ingredients_list = []

    # Fetch or create manufacturer
    manufacturer = None
    if manufacturer_name:
        contact_data = get_manufacturer_contacts(manufacturer_name)
        website = contact_data.get("website")
        email = contact_data.get("emails", [None])[0]
        phone = contact_data.get("phones", [None])[0]

        manufacturer, _ = Manufacturer.objects.get_or_create(
            name=manufacturer_name,
            defaults={
                "website": website,
                "contact_email": email,
                "contact_phone": phone,
            },
        )

    # Save product
    product, _ = Product.objects.get_or_create(
        name=product_name,
        defaults={
            "manufacturer": manufacturer,
            "category": None,
            "website": url,
            "store_name": (
                urlparse(url).query.split("retailerSlug=")[-1]
                if "retailerSlug=" in url
                else None
            ),
        },
    )

    # Save ingredients and mapping
    for ingredient_name in ingredients_list:
        ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
        IngredientProduct.objects.get_or_create(product=product, ingredient=ingredient)

    print(f"✅ Saved: {product_name} | Manufacturer: {manufacturer_name}")

driver.quit()
