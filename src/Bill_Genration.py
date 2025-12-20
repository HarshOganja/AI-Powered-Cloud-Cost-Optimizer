import json
import os
import requests

file="data/output/Billing_Generation.json"
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise RuntimeError("HF_API_KEY not found in environment")
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
- PLUS generate EXACTLY TWO (2) additional services
- Additional services MUST be reasonable baseline infrastructure
- Additional services MUST be derived from non_functional_requirements
- DO NOT invent unrelated services
- DO NOT add CDN, DNS, Lambda, AI, or advanced services
- EACH service must appear ONLY ONCE
- ONE billing record = ONE clear responsibility
===========================================================

================= ALLOWED ADDITIONAL SERVICES =================
You may ONLY choose from this list for the 2 extra services:
- logging
- load_balancing
- backup
- basic_security
- caching
- monitoring (only if not already present)
===============================================================

================= BUDGET REALISM RULES =================
- Monthly budget is given in the project profile
- TOTAL monthly cost MUST fall between:
    70% and 120% of the stated budget
- It MAY be under or over budget, but must remain realistic
- No single service should exceed 50% of the total cost
- Costs should reflect typical small-to-mid scale production usage
========================================================

================= FIELD MAPPING RULES =================
- "serves" MUST be:
  - a tech_stack key OR
  - one of the additional service names exactly as listed above
- "desc" must clearly explain what that service does
- Costs must be realistic, balanced, and budget-aware
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
- Exactly TWO additional services included
- Total cost is between 70%–120% of budget
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
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'w') as f:
        json.dump(json.loads(response.json()["choices"][0]["message"]["content"]), f,indent=4)
        
    raw_output = response.json()["choices"][0]["message"]["content"]

    try:
        start = raw_output.index("[")
        end = raw_output.rindex("]") + 1
        return json.loads(raw_output[start:end])
    except Exception as e:
        raise ValueError(
            f"LLM did not return valid JSON billing data.\nRaw output:\n{raw_output}"
        ) from e
