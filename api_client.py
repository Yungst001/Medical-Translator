
import requests


# ==========================================
# CUSTOM API ERRORS
# ==========================================

class OpenFDAError(Exception):
    """General error from the OpenFDA client."""
    pass


class DrugNotFoundError(OpenFDAError):
    """Raised when no matching drug label is found."""
    pass


# ==========================================
# OPENFDA API CLIENT
# ==========================================

class OpenFDAClient:

    BASE_URL = "https://api.fda.gov"

    # --------------------------------------
    # Prepare user input for FDA search
    # --------------------------------------

    @staticmethod
    def _clean_drug_name(drug_name):

        if not isinstance(drug_name, str):
            raise ValueError("Drug name must be text.")

        drug_name = drug_name.strip()

        if not drug_name:
            raise ValueError("Please enter a drug name.")

        # Escape characters that can affect search syntax
        special_chars = r'+-&|!(){}[]^"~*?:\/'

        cleaned_name = ""

        for char in drug_name:
            if char in special_chars:
                cleaned_name += "\\"

            cleaned_name += char

        return cleaned_name

    # --------------------------------------
    # Fetch drug label information
    # --------------------------------------

    @staticmethod
    def fetch_drug_label(drug_name):

        drug_name = OpenFDAClient._clean_drug_name(drug_name)

        url = f"{OpenFDAClient.BASE_URL}/drug/label.json"

        params = {
            "search": (
                f'openfda.brand_name:"{drug_name}" '
                f'OR openfda.generic_name:"{drug_name}"'
            ),
            "limit": 1
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            if response.status_code == 404:
                raise DrugNotFoundError(
                    f"No drug label found for '{drug_name}'."
                )

            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            if not results:
                raise DrugNotFoundError(
                    f"No drug information found for '{drug_name}'."
                )

            return results[0]

        except requests.exceptions.Timeout as error:
            raise OpenFDAError(
                "The FDA server took too long to respond."
            ) from error

        except requests.exceptions.ConnectionError as error:
            raise OpenFDAError(
                "Unable to connect to the FDA server. Check your internet."
            ) from error

        except requests.exceptions.RequestException as error:
            raise OpenFDAError(
                f"FDA request failed: {error}"
            ) from error

        except ValueError as error:
            raise OpenFDAError(
                "The FDA returned an invalid response."
            ) from error

    # --------------------------------------
    # Fetch ongoing drug recalls
    # --------------------------------------

    @staticmethod
    def fetch_drug_recall(drug_name):

        drug_name = OpenFDAClient._clean_drug_name(drug_name)

        url = f"{OpenFDAClient.BASE_URL}/drug/enforcement.json"

        params = {
            "search": f'product_description:"{drug_name}"',
            "limit": 100
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            # No matching enforcement records
            if response.status_code == 404:
                return []

            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            # Keep only ongoing recalls
            ongoing_recalls = [
                recall for recall in results
                if recall.get("status", "").lower() == "ongoing"
            ]

            return ongoing_recalls

        except requests.exceptions.Timeout as error:
            raise OpenFDAError(
                "Recall search timed out."
            ) from error

        except requests.exceptions.ConnectionError as error:
            raise OpenFDAError(
                "Unable to connect to the FDA recall service."
            ) from error

        except requests.exceptions.RequestException as error:
            raise OpenFDAError(
                f"Recall request failed: {error}"
            ) from error

        except ValueError as error:
            raise OpenFDAError(
                "Invalid recall information received."
            ) from error

    # --------------------------------------
    # Extract useful drug information
    # --------------------------------------

    @staticmethod
    def get_drug_information(drug_name):

        label = OpenFDAClient.fetch_drug_label(drug_name)

        openfda = label.get("openfda", {})

        def get_first_value(value):

            if isinstance(value, list):
                return value[0] if value else "Not available"

            return value if value else "Not available"

        information = {
            "brand_name": get_first_value(
                openfda.get("brand_name")
            ),

            "generic_name": get_first_value(
                openfda.get("generic_name")
            ),

            "manufacturer": get_first_value(
                openfda.get("manufacturer_name")
            ),

            "uses": get_first_value(
                label.get("indications_and_usage")
            ),

            "warnings": get_first_value(
                label.get("warnings")
            ),

            "side_effects": get_first_value(
                label.get("adverse_reactions")
            ),

            "contraindications": get_first_value(
                label.get("contraindications")
            ),

            "dosage": get_first_value(
                label.get("dosage_and_administration")
            ),

            "drug_interactions": get_first_value(
                label.get("drug_interactions")
            )
        }

        return information
