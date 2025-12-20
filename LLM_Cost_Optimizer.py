import json
from src.Profile_Extraction import profile_extraction
from src.Bill_Genration import generate_synthetic_billing
from src.Recommendation import generate_llm_recommendations
from src.Html_Report import export_html_report
import os


def Enter_Description():
    print("Enter your Project Description (press Enter twice to submit):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    description = "\n".join(lines)
    return description


def Profile_Extraction():
    description = Enter_Description()
    try:
        project_profile = profile_extraction(description)
        print("\n=== EXTRACTED PROJECT PROFILE JSON ===")
        print(json.dumps(project_profile, indent=4))
        return project_profile
    except Exception as e:
        print("\nERROR in Profile Extraction:", e)
        return None
    
    
def Bill_Genration(project_profile):
    try:
        billing_records = generate_synthetic_billing(project_profile)
        print("\n=== SYNTHETIC BILLING (LLM-GENERATED) ===")
        print(json.dumps(billing_records, indent=4))
        return billing_records
    except Exception as e:
        print("\nERROR in Bill Generation:", e)
        return None
    
    
def cost_analysis(billing_records,project_profile ):
    total_cost = sum(r["cost_inr"] for r in billing_records)
    service_costs = {r["service"]: r["cost_inr"] for r in billing_records}
    analysis = {
        "budget": project_profile["budget_inr_per_month"],
        "total_cost": total_cost,
        "service_costs": service_costs,
        "is_over_budget": total_cost > project_profile["budget_inr_per_month"]
    }
    print("\n=== Cost Analysis ===")
    print(json.dumps(analysis, indent=4))
    return analysis 


def Recommendation(project_profile, billing_records, cost_analysis):
    try:
        recommend=generate_llm_recommendations(project_profile,billing_records,cost_analysis)
        print("\n=== Recommendations ===")
        print(json.dumps(recommend, indent=4))
        return recommend
    except Exception as e:
        print("\nERROR in Recommendation Generation:", e)
        return None


def main():
    while True:
        print("""
================ Cloud Cost Optimizer =================
1. Enter new project description and extract profile
2. Generate synthetic billing and cost analysis
3. Generate optimization recommendations
4. Export full report as JSON and HTML
5. Exit
======================================================
""")
        input_choice = input("Select an option (1-5), Make sure to choice in correct order: ").strip()
        if input_choice == "1":
            project_profile = Profile_Extraction()
        elif input_choice == "2":
            if 'project_profile' not in locals() or project_profile is None:
                print("\nPlease extract project profile first (Option 1).")
                continue
            billing_records = Bill_Genration(project_profile)
            if billing_records:
                cost_analysis_data = cost_analysis(billing_records,project_profile)
                
        elif input_choice == "3":
            if 'project_profile' not in locals() or project_profile is None:
                print("\nPlease extract project profile first (Option 1).")
                continue
            if 'billing_records' not in locals() or billing_records is None:
                print("\nPlease generate billing records first (Option 2).")
                continue
            recommend=Recommendation(project_profile, billing_records, cost_analysis_data)
        elif input_choice == "4":
            if 'project_profile' not in locals() or project_profile is None:
                print("\nPlease extract project profile first (Option 1).")
                continue
            if 'billing_records' not in locals() or billing_records is None:
                print("\nPlease generate billing records first (Option 2).")
                continue
            if 'recommend' not in locals() or recommend is None:
                print("\nPlease generate recommendations first (Option 3).")
                continue
            final_report = {
            "project_profile": project_profile,
                "billing": billing_records,
                "analysis": cost_analysis_data,
                "recommendations": recommend
            }
            json_path = f"data/output/cost_optimization_report.json"
            html_path = f"data/output/cost_optimization_report.html"

            with open(json_path, "w") as f:
                json.dump(final_report, f, indent=4)

            export_html_report(final_report, html_path)

            print("JSON report exported")
            print("HTML report exported")
        elif input_choice == "5":
            print("Exiting Cloud Cost Optimizer. Goodbye!")
            break
        else:
            print("\n\n\nInvalid choice. Please select a valid option (1-5).\n\n")
main()
