import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from app.retriever import retrieve
from app.prompts import SYSTEM_PROMPT

# Configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Load catalog in memory for validation and post-processing
with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f, strict=False)

# Build lookups for post-processing
catalog_by_url = {item['url'].lower(): item for item in catalog if item.get('url')}
catalog_by_name = {item['name'].lower(): item for item in catalog if item.get('name')}


def build_context(documents):
    """
    Convert retrieved catalog entries into prompt context.
    """
    context = ""
    for doc in documents:
        # Construct a detailed context block for each document
        job_levels = doc.get('job_levels', [])
        if not isinstance(job_levels, list):
            job_levels = []
        languages = doc.get('languages', [])
        if not isinstance(languages, list):
            languages = []
        keys = doc.get('keys', [])
        if not isinstance(keys, list):
            keys = []

        context += f"""Name: {doc.get('name', '')}
Type: {doc.get('test_type', '')}
URL: {doc.get('url', '')}
Keys: {', '.join(keys)}
Job Levels: {', '.join(job_levels)}
Languages: {', '.join(languages)}
Duration: {doc.get('duration', '')}
Description: {doc.get('description', '')}
-------------------------\n"""
    return context


def build_prompt(messages, context):
    """
    Build the complete prompt for Gemini.
    """
    # Format the message history into a clear dialog format
    formatted_history = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted_history += f"{role}: {msg['content']}\n\n"

    return f"""{SYSTEM_PROMPT}

=========================
SHL CATALOG CONTEXT
=========================
Below is the subset of SHL assessments retrieved from the catalog based on relevance. Use ONLY these assessments to recommend or discuss:

{context}

=========================
CONVERSATION HISTORY
=========================
Read the conversation history below:

{formatted_history}

=========================
OUTPUT REQUIREMENT
=========================
You MUST respond with a single JSON object. Do not include any explanations or markdown wrappers outside the JSON. The JSON must exactly match the schema below:
{{
  "reply": "Your response text to the user. It should clarify, explain, compare, or confirm constraints based on rules.",
  "recommendations": [
    {{
      "name": "Exact assessment name",
      "url": "Exact catalog URL from the catalog context",
      "test_type": "Exact test_type from the catalog context"
    }}
  ],
  "end_of_conversation": true_or_false
}}

Remember:
- recommendations list must be empty (i.e. []) if you are asking a clarification question, refusing, or if the user is not finalized.
- end_of_conversation is true only if the user confirms satisfaction or locks in the list.
"""


def chat(messages):
    """
    Main chat function.
    """
    # Find latest user message
    last_user_message = ""
    for message in reversed(messages):
        if message["role"] == "user":
            last_user_message = message["content"]
            break

    # Retrieve relevant assessments
    documents = retrieve(last_user_message, messages, k=40)

    # Build context
    context = build_context(documents)

    # Build final prompt
    prompt = build_prompt(messages, context)

    try:
        # Call Gemini with JSON constraint
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        text = response.text.strip()

        # Convert JSON text to Python dictionary
        result = json.loads(text)

        # Enforce and sanitize required keys
        result.setdefault("reply", "")
        result.setdefault("recommendations", [])
        result.setdefault("end_of_conversation", False)

        # Post-process recommendations to guarantee grounding, catalog correctness, and prevent hallucinations
        validated_recs = []
        seen_rec_urls = set()

        for rec in result.get("recommendations", []):
            name = rec.get("name", "")
            url = rec.get("url", "")
            
            # Find closest item in the catalog
            matched_item = None
            if url and url.lower() in catalog_by_url:
                matched_item = catalog_by_url[url.lower()]
            elif name and name.lower() in catalog_by_name:
                matched_item = catalog_by_name[name.lower()]
            else:
                # Substring match fallback
                for cat_name, cat_item in catalog_by_name.items():
                    if name.lower() in cat_name or cat_name in name.lower():
                        matched_item = cat_item
                        break

            if matched_item:
                target_url = matched_item["url"]
                if target_url not in seen_rec_urls:
                    seen_rec_urls.add(target_url)
                    validated_recs.append({
                        "name": matched_item["name"],
                        "url": target_url,
                        "test_type": matched_item["test_type"]
                    })

        result["recommendations"] = validated_recs

        return result

    except Exception as e:
        print("Gemini Error:", e)
        return {
            "reply": "Sorry, I encountered an issue processing your request. Could you please rephrase or try again?",
            "recommendations": [],
            "end_of_conversation": False
        }