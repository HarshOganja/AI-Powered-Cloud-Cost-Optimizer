import json
from Profile_Extraction import profile_extraction
from Bill_Genration import generate_synthetic_billing
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
    except Exception as e:
        print("\nERROR:", e)

main()
