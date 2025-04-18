import email
import os
import requests
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

chat_history = []


def get_manufacturer_website(manufacturer_name):
    """Fetch the official website of the manufacturer using SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{manufacturer_name} official site",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params)
    results = response.json()

    for result in results.get("organic_results", []):
        if (
            "official" in result["title"].lower()
            or "contact" in result["title"].lower()
        ):
            return result["link"]

    return None


def get_contact_details(manufacturer_name):
    """Fetch email and phone number from Google Search using SerpAPI"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"{manufacturer_name} contact email phone",
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params)
    results = response.json()

    emails, phones = set(), set()

    for result in results.get("organic_results", []):
        text = result.get("snippet", "")

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails.update(re.findall(email_pattern, text))

        phone_pattern = r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4,6}"
        phones.update(re.findall(phone_pattern, text))

    return {"emails": list(emails), "phones": list(phones)}


def generate_response(user_input):
    """Use Gemini AI if email or phone is missing"""
    global chat_history

    if not user_input.strip():
        return None

    # Maintain chat history
    history_context = "\n".join(
        [
            f"User: {entry['user']}\nAssistant: {entry['assistant']}"
            for entry in chat_history
        ]
    )

    model = genai.GenerativeModel(  # type: ignore
        model_name="gemini-2.0-flash",
        generation_config={
            "temperature": 0.1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
        },  # type: ignore
        system_instruction="Only provide phone number and email separated by comma of the given manufacturer. If not found, keep it as none.This is highly important don't give any invalid email.",
    )

    prompt = f"History:\n{history_context}\n\nUser: {user_input}\nAssistant:"

    try:
        response = model.generate_content(prompt)
        assistant_reply = response.text.strip()
    except Exception as e:
        return None

    chat_history.append({"user": user_input, "assistant": assistant_reply})

    return assistant_reply


def get_manufacturer_contacts(manufacturer_name):
    """Fetch website, email, and phone, using Gemini AI as a fallback."""
    website = get_manufacturer_website(manufacturer_name)
    contact_info = get_contact_details(manufacturer_name)
    # contact_info = {"emails": [], "phones": []}
    if not contact_info["emails"] or not contact_info["phones"]:
        ai_response = generate_response(manufacturer_name)
        if ai_response and "," in ai_response:
            phone, email = ai_response.split(",")
            if not contact_info["emails"]:
                contact_info["emails"].append(email.strip())
            if not contact_info["phones"]:
                contact_info["phones"].append(phone.strip())

    return {
        "website": website,
        "emails": contact_info["emails"],
        "phones": contact_info["phones"],
    }
