import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
model_id="meta-llama/Meta-Llama-3-8B-Instruct"
def profile_extraction(description):
    prompt = f"""You are an AI that extracts structured project metadata.
    You MUST return STRICT JSON ONLY.
    NO explanation. NO markdown. NO text outside JSON.

    Required structure:
    {{
    "name": string,
    "budget_inr_per_month": number or null,
    "description": string,
    "tech_stack": object (dynamic keys, inferred from text),
    "non_functional_requirements": [string]
    }}

    Rules:
    - "tech_stack" must NOT use any predefined keys; infer meaningful ones.
    - "name" must be a short inferred title.
    - If no budget found → use null.
    - Output MUST be valid JSON. No trailing commas.

    Extract from this description:
    \"\"\"{description}\"\"\"
    """
    url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500},
        "options": {"use_cache": True}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    raw_output = result[0]["generated_text"]

    # Extract JSON safely (model may wrap text)
    try:
        json_start = raw_output.index("{")
        json_end = raw_output.rindex("}") + 1
        cleaned = raw_output[json_start:json_end]
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"LLM did not return valid JSON.\nRaw output:\n{raw_output}") from e