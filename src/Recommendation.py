import os
import requests
import json


HF_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"
file="data/output/Recommendation.json"
def generate_llm_recommendations(project_profile, billing_records, cost_analysis):
    prompt = f"""
You are an AI system that generates CLOUD COST OPTIMIZATION RECOMMENDATIONS.

==================== OUTPUT FORMAT ====================
YOU MUST FOLLOW THESE RULES STRICTLY:

1. OUTPUT MUST BE VALID JSON ONLY
2. OUTPUT MUST BE A SINGLE JSON OBJECT
3. DO NOT include markdown
4. DO NOT include explanations
5. DO NOT include text outside JSON
6. DO NOT repeat keys
7. DO NOT hallucinate services
=======================================================

==================== REQUIRED JSON SCHEMA ====================
{{
  "project_name": string,
  "analysis": {{
    "total_monthly_cost": number,
    "budget": number,
    "budget_variance": number,
    "service_costs": object,
    "high_cost_services": object,
    "is_over_budget": boolean
  }},
  "recommendations": [
    {{
      "title": string,
      "service": string,
      "current_cost": number,
      "potential_savings": number,
      "recommendation_type": "optimization" | "open_source" | "free_tier" | "alternative_provider" | "right_sizing",
      "description": string,
      "implementation_effort": "low" | "medium" | "high",
      "risk_level": "low" | "medium" | "high",
      "steps": [string],
      "cloud_providers": [string]
    }}
  ],
  "summary": {{
    "total_potential_savings": number,
    "savings_percentage": number,
    "recommendations_count": number,
    "high_impact_recommendations": number
  }}
}}
==============================================================

==================== GENERATION RULES ====================
- Generate 6 to 10 recommendations
- Recommendations MUST be multi-cloud (AWS, Azure, GCP, OpenText, Open-source)
- Potential savings must be realistic (not 100%)
- Base analysis STRICTLY on billing data
- Do NOT invent services not present in billing
- Budget variance must match computed values
==========================================================

==================== INPUT DATA ====================
Project Profile:
{json.dumps(project_profile, indent=2)}

Billing Records:
{json.dumps(billing_records, indent=2)}

Cost Analysis:
{json.dumps(cost_analysis, indent=2)}
====================================================

FINAL CHECK BEFORE RESPONDING:
- Output is valid JSON
- Matches schema exactly
- No text outside JSON

RESPOND WITH JSON ONLY.
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
        "temperature": 0.3,
        "max_tokens": 1500
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    if os.path.exists(file):
        os.remove(file)
    with open(file, 'w') as f:
        json.dump(json.loads(response.json()["choices"][0]["message"]["content"]), f,indent=4)
    data = response.json()

    raw_text = data["choices"][0]["message"]["content"]

    try:
        recommendations_json = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON:\n" + raw_text)

    return recommendations_json
