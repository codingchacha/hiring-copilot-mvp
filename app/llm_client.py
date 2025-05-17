from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.environ.get("API_KEY"))

def prompt_to_candidate_query(user_prompt: str) -> dict:
    """
    Uses LLM to convert a natural language user prompt into a candidate search query filter.

    Args:
        user_prompt (str): The user input describing desired candidate skills, experience, location, etc.

    Returns:
        dict: A structured query dict (JSON) for filtering candidates.
    """
    system_msg = (
        "You are an AI assistant that converts hiring manager prompts into a JSON query "
        "for filtering candidates. Respond ONLY with valid, raw JSON (no explanation, no markdown, "
        "no ``` or ```json). The JSON keys can include: experience (int), skills (list), "
        "location (str), github_stars_min (int), certifications (list)."
    )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_prompt}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        top_p=0.9,
    )

    raw_response = chat_completion.choices[0].message.content


    # Clean up LLM output: remove backticks and "json" tag if included
    cleaned = raw_response.strip().replace("```json", "").replace("```", "").strip()
    

    try:
        query_json = json.loads(cleaned)
    except json.JSONDecodeError:
        query_json = {}

    return query_json
