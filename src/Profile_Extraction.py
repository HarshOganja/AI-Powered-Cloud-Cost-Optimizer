import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"
file="data/output/Profile_Extraction.json"

def profile_extraction(description):
    prompt = f"""You are an AI that extracts structured project metadata.
You MUST return STRICT JSON ONLY.
NO explanation. NO markdown. NO text outside JSON.

Required structure:
{{
  "name": string,
  "budget_inr_per_month": number or null,
  "description": string,
  "tech_stack": object,
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

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "max_tokens": 600
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'w') as f:
        json.dump(json.loads(response.json()["choices"][0]["message"]["content"]), f,indent=4)
    result = response.json()
    
    raw_output = result["choices"][0]["message"]["content"]
    try:
        json_start = raw_output.index("{")
        json_end = raw_output.rindex("}") + 1
        cleaned = raw_output[json_start:json_end]
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(
            f"LLM did not return valid JSON.\nRaw output:\n{raw_output}"
        ) from e
