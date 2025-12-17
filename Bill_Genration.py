import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"

def generate_synthetic_billing(project_profile: dict) -> list:
    prompt = f"""
You are an AI that generates CLEAN, REALISTIC, SYNTHETIC cloud billing data.

================= OUTPUT RULES =================
- Output MUST be STRICT JSON ONLY
- Output MUST be a JSON ARRAY
- NO markdown
- NO explanation
- NO duplicate keys
================================================

================= PROVIDER SELECTION =================
1. If "hosting_platform" or "cloud_platform" exists in the project profile:
   - Use ONLY services from that provider
   - DO NOT include OpenText services

2. If NO hosting/cloud platform is mentioned:
   - Use OpenText Cloud as the DEFAULT and ONLY provider

3. NEVER mix cloud providers under any condition
======================================================

================= SERVICE GENERATION RULES =================
- Generate EXACTLY ONE billing record per tech_stack item
- DO NOT invent additional services
- DO NOT add CDN, DNS, Lambda, Backup, Security, etc. unless explicitly present
- EACH service must appear ONLY ONCE
- ONE billing record = ONE clear responsibility
===========================================================
================= FIELD MAPPING RULES =================
- "serves" MUST exactly match a key from "tech_stack"
- "desc" must clearly explain what that service does
- Costs must be realistic and respect the monthly budget
=======================================================

================= REQUIRED JSON STRUCTURE =================
Each object in the array MUST follow this schema:

{{
  "month": "YYYY-MM",
  "service": string,
  "resource_id": string,
  "region": string,
  "usage_type": string,
  "usage_quantity": number,
  "unit": string,
  "cost_inr": number,
  "serves": string,
  "desc": string
}}
===========================================================

FINAL VALIDATION CHECK (MANDATORY):
- Provider rules strictly followed
- One service per tech_stack item
- No duplicated services
- No duplicated keys
- Valid JSON array ONLY

Project profile:
{json.dumps(project_profile, indent=2)}

Output ONLY the JSON array.
"""

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 1200
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    raw_output = response.json()["choices"][0]["message"]["content"]

    try:
        start = raw_output.index("[")
        end = raw_output.rindex("]") + 1
        return json.loads(raw_output[start:end])
    except Exception as e:
        raise ValueError(
            f"LLM did not return valid JSON billing data.\nRaw output:\n{raw_output}"
        ) from e
