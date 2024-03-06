import requests
import sys
import time

def display_signature_progress(completion, total, bar_width=10):
    bar_slots = "🍒🍋🔔💰🚁🛩️🛸🚀🛰️"
    drone_str = "DRONE2MAX!"
    slots_filled = int((completion / total) * bar_width)
    bar_str = drone_str[:slots_filled] + bar_slots[((completion % len(bar_slots)) - 1) % len(bar_slots)] * (bar_width - slots_filled)
    bar_str = bar_str[:bar_width]

    sys.stdout.write(f'\r[{bar_str}] {completion}/{total} completed')
    sys.stdout.flush()

session = requests.Session()

def get_scientific_classification(name: str, filter_order: str = None) -> (bool, dict):
    """Fetches the scientific classification for a given name from the GBIF API, optionally filtering by order.

    Args:
        name (str): The scientific name to query.
        filter_order (str, optional): A specific order to filter the results by.

    Returns:
        tuple: A boolean indicating success, and a dictionary with classification details if successful.
    """
    try:
        response = requests.get(f"https://api.gbif.org/v1/species/match?name={name}&strict=true")
        response.raise_for_status()
        data = response.json()
        if data.get("matchType") != "NONE":
            if filter_order and data.get("order") != filter_order:
                return False, None
            classification = {"order": data.get("order"), "family": data.get("family"), "genus": data.get("genus")}
            return True, classification
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return False, None

def filter_words_by_order(file_path: str, filter_order: str, output_file: str) -> None:
    """Filters words by scientific order, saving matches to an output file.

    Args:
        file_path (str): Path to the input file containing words to check.
        filter_order (str): The taxonomic order to filter results by.
        output_file (str): Path to the output file for saving matches.
    """
    try:
        with open(file_path, "r") as file:
            words = [line.strip() for line in file]

        total_words = len(words)
        filtered_words = []

        for i, word in enumerate(words, 1):
            is_scientific, classification = get_scientific_classification(word, filter_order)
            display_signature_progress(i, total_words)
            if is_scientific:
                filtered_words.append(word)
                print(f"\n{word} matches criteria: {classification}")

        with open(output_file, "w") as file:
            file.write("\n".join(filtered_words))

        print(f"\nFiltered words have been saved to {output_file}")
    except IOError as e:
        print(f"\nAn error occurred while handling files: {e}")


# Example usage
file_path = r".\dirty_classes.txt"
output_file = "cleaned_classes.txt"  # Name of the file to save the filtered words
filter_order = "Pinales"  # Specify the order you're interested in
filter_words_by_order(file_path, filter_order, output_file)
