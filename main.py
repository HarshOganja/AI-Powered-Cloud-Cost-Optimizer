import json
from Profile_Extraction import profile_extraction
from Bill_Genration import generate_synthetic_billing
from Recommendation import generate_llm_recommendations
def main():
    print("Enter your Project Description (press Enter twice to submit):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    description = "\n".join(lines)
    try:
        project_profile = profile_extraction(description)
        print("\n=== EXTRACTED PROJECT PROFILE JSON ===")
        print(json.dumps(project_profile, indent=4))
        billing_records = generate_synthetic_billing(project_profile)
        print("\n=== SYNTHETIC BILLING (LLM-GENERATED) ===")
        print(json.dumps(billing_records, indent=4))
        print("\n=== Cost Analysis ===")
        cost_analysis = {
        "total_cost": sum(r["cost_inr"] for r in billing_records),
        "service_costs": {
            r["service"]: r["cost_inr"] for r in billing_records
        }}
        budget=project_profile["budget_inr_per_month"]
        print("\nTotal Cost  ",cost_analysis["total_cost"])
        print("\nBudget Per Month  ",budget)
        print("\nVarience",cost_analysis["total_cost"]-budget)
        recommend=generate_llm_recommendations(project_profile,billing_records,cost_analysis)
        print("\n=== Recommendations ===")
        print(json.dumps(recommend, indent=4))
    except Exception as e:
        print("\nERROR:", e)

main()
