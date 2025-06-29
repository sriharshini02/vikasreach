import google.generativeai as genai
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore


# Maintain chat history for continuity if needed
chat_history = []


def get_products_from_raw_material(raw_material):
    """
    Uses Gemini to generate a list of products that can be made
    from the given raw material.
    """
    global chat_history

    if not raw_material.strip():
        return []

    # Maintain chat history context
    history_context = "\n".join(
        [
            f"User: {entry['user']}\nAssistant: {entry['assistant']}"
            for entry in chat_history
        ]
    )

    model = genai.GenerativeModel(  # type: ignore
        model_name="gemini-2.0-pro-exp-02-05",
        generation_config={
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 512,
        },  # type: ignore
        system_instruction=(
            "Provide a comma-separated list of 1 to 5 products that can be manufactured using the given raw material. Only return the product names without descriptions."
        ),
    )

    prompt = f"History:\n{history_context}\n\nUser: What products can be made using {raw_material}?\nAssistant:"

    try:
        response = model.generate_content(prompt)
        assistant_reply = response.text.strip()
    except Exception as e:
        return []

    chat_history.append({"user": raw_material, "assistant": assistant_reply})

    # Clean and return list of products
    products = [item.strip() for item in assistant_reply.split(",") if item.strip()]
    print(products)
    return products


if __name__ == "__main__":
    print(get_products_from_raw_material("sugar"))
