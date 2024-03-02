import requests

def get_scientific_classification(name, filter_order=None):
    response = requests.get(f"https://api.gbif.org/v1/species/match?name={name}&strict=true")
    if response.status_code == 200:
        data = response.json()
        if data.get('matchType') != 'NONE':
            # Check if a specific order filter is applied and if the matched name belongs to that order
            if filter_order and data.get('order') != filter_order:
                return False, None  # Name does not belong to the specified order
            classification = {
                "kingdom": data.get("kingdom"),
                "phylum": data.get("phylum"),
                "class": data.get("class"),  # Added class to the classification
                "order": data.get("order"),
                "family": data.get("family"),
                "genus": data.get("genus"),
                "species": data.get("species")
            }
            return True, classification
    return False, None

# Example usage
name_to_check = "Abies"
filter_order = "Pinales"  # Specify the order you want to filter by
is_scientific, classification = get_scientific_classification(name_to_check, filter_order=filter_order)

if is_scientific:
    print(f"{name_to_check} is a scientific name with classification: {classification}")
else:
    print(f"{name_to_check} is not a scientific name or does not belong to the order {filter_order}.")
