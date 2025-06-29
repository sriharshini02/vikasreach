import google.generativeai as genai
from dotenv import load_dotenv
import ast
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore


import google.generativeai as genai
import re


def get_keyword_to_ingredient_ids(user_query, ingredient_list):
    if not user_query.strip() or not ingredient_list:
        return {}

    model = genai.GenerativeModel("gemini-2.0-flash")  # type: ignore

    formatted_ingredients = "\n".join(
        [f"{id} -> {name}" for id, name in ingredient_list]
    )

    keywords = [kw.strip() for kw in user_query.lower().split(",") if kw.strip()]
    result = {}

    for keyword in keywords:
        prompt = f"""
You are an expert at ingredient matching.

User keyword: "{keyword}"

Here is a list of ingredient names from the database with their IDs:
{formatted_ingredients}

Your task: Return a Python list of IDs of ingredients that are strictly matched and have completely same meaning as the given ingredient without any misunderstanding.
For example : cotton candy and cotton are not same. Most importantly we can't consider empty string as a match. 
Only return a list like: [1, 2, 5]. If no matches, return an empty list: []
Don't return any extra text, explanation, or formatting.
"""

        try:
            response = model.generate_content(prompt)
            output = response.text.strip()
            match = re.search(r"\[([\d,\s]+)\]", output)
            if match:
                id_list = [
                    int(i.strip()) for i in match.group(1).split(",") if i.strip()
                ]
                result[keyword] = id_list
            else:
                result[keyword] = []
        except Exception as e:
            print(f"❌ Gemini error for '{keyword}':", e)
            result[keyword] = []
    print(result)
    return result


if __name__ == "__main__":

    ingredients_from_db = [
        (1, "milk powder"),
        (2, "sunflower oil"),
        (3, "refined oil"),
        (4, "skimmed milk"),
        (5, "coconut flour"),
    ]

    query = "milk, oil, sugar"
    matched_dict = get_keyword_to_ingredient_ids(query, ingredients_from_db)

    print(matched_dict)
    # ➜ {'milk': [1, 4], 'oil': [2, 3], 'sugar': []}