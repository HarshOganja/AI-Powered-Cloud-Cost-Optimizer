import json
from Profile_Extraction import profile_extraction
def main():
    print("Enter your Project Description")
    description=input()
    try:
        result = profile_extraction(description)
        print("=== EXTRACTED PROJECT PROFILE JSON ===")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print("\nERROR:", e) 
main()