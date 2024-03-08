import requests
from typing import Tuple, Dict, Union


def get_scientific_classification(name: str, filter_order: str = None) -> Tuple[bool, Union[Dict[str, str], None]]:
    """
    Fetches the scientific classification for a given name from the GBIF API.

    Parameters:
    - name (str): The scientific name to query.
    - filter_order (str, optional): A specific order to filter the results by.

    Returns:
    - tuple: A boolean indicating if a match was found (and optionally matched the filter_order),
             and a dictionary with the classification details or None if no match was found.
    """
    try:
        response = requests.get(f"https://api.gbif.org/v1/species/match?name={name}&strict=true")
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()
        if data.get('matchType') != 'NONE':
            if filter_order and data.get('order') != filter_order:
                return False, None  # Name does not match the specified order

            classification = {
                "kingdom": data.get("kingdom"),
                "phylum": data.get("phylum"),
                "class": data.get("class"),
                "order": data.get("order"),
                "family": data.get("family"),
                "genus": data.get("genus"),
                "species": data.get("species")
            }
            return True, classification
    except requests.RequestException as e:
        print(f"Request to GBIF API failed: {e}")
    return False, None