
from api_client import OpenFDAClient
import requests

drug_name = "Aspirin"

print("MEDICAL INFORMATION TRANSLATOR")
print("=" * 35)

try:
    # Fetch drug label
    print("\nFetching drug information...")

    label = OpenFDAClient.fetch_drug_label(drug_name)

    print("Drug label retrieved successfully!")

    print("\nDRUG INFORMATION")

    openfda = label.get("openfda", {})

    print("Brand:", openfda.get("brand_name", ["N/A"])[0])
    print("Generic:", openfda.get("generic_name", ["N/A"])[0])

    print("\nUSES:")
    print("\n".join(label.get("indications_and_usage", ["Not available"])))

    print("\nWARNINGS:")
    print("\n".join(label.get("warnings", ["Not available"])))

    print("\nSIDE EFFECTS:")
    print("\n".join(label.get("adverse_reactions", ["Not available"])))

    # Fetch recalls
    print("\nChecking ongoing recalls...")

    recalls = OpenFDAClient.fetch_drug_recall(drug_name)

    if recalls:
        print(f"\n{len(recalls)} ongoing matching recall record(s) found.")

        for recall in recalls:
            print("\nRecall number:", recall.get("recall_number", "N/A"))
            print("Reason:", recall.get("reason_for_recall", "N/A"))
            print("Status:", recall.get("status", "N/A"))

    else:
        print("No ongoing matching recall records found.")

except ValueError as e:
    print("Input or search error:", e)

except requests.exceptions.RequestException as e:
    print("Network/API error:", e)

except Exception as e:
    print("Unexpected error:", type(e).__name__, e)

print("\nAPI TEST COMPLETED.")
