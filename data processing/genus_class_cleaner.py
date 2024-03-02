import requests
from tqdm import tqdm


def get_scientific_classification(name, filter_order=None):
    """
    Checks if a given name matches a scientific classification in the GBIF database,
    optionally filtering by the specified order.

    Parameters:
    - name: The scientific name to check.
    - filter_order: The taxonomic order to filter results by (optional).

    Returns:
    - A tuple (bool, dict): First element is True if the name matches and passes the filter (if applied),
    and False otherwise. The second element is a dictionary containing the classification details if a match is found.
    """
    # Make a request to the GBIF species match API with the provided name
    response = requests.get(
        f"https://api.gbif.org/v1/species/match?name={name}&strict=true"
    )
    if response.status_code == 200:  # Check if the request was successful
        data = response.json()  # Parse the JSON response
        if data.get("matchType") != "NONE":  # Check if there was a match
            # Apply the order filter if specified
            if filter_order and data.get("order") != filter_order:
                return False, None  # If the order does not match, return False
            # Construct a dictionary with the classification details
            classification = {
                "order": data.get("order"),
                "family": data.get("family"),
                "genus": data.get("genus"),
            }
            return True, classification  # Return True and the classification details
    return False, None  # Return False if no match was found or the request failed


def filter_words_by_order(file_path, filter_order, output_file):
    """
    Reads words from a text file, checks each against the GBIF database for scientific classification,
    and filters them by the specified order. The filtered words are then saved to another text file.

    Parameters:
    - file_path: Path to the input text file containing words to check.
    - filter_order: The taxonomic order to filter results by.
    - output_file: Path to the output text file where filtered words will be saved.
    """
    # Read words from the input file
    with open(file_path, "r") as file:
        words = file.read().splitlines()

    filtered_words = []
    for word in tqdm(words, desc="Processing", unit="word"):
        is_scientific, classification = get_scientific_classification(
            word, filter_order=filter_order
        )
        if is_scientific:
            filtered_words.append(word)
            sentence = (
                f"The word '{word}' belongs to the order '{classification.get('order')}', "
                f"family '{classification.get('family')}', "
                f"genus '{classification.get('genus')}'. "
            )
            tqdm.write(
                sentence
            )  # Use tqdm.write to print the sentence without disrupting the progress bar.

    with open(output_file, "w") as file:
        for word in filtered_words:
            file.write(word + "\n")
    tqdm.write(
        f"Filtered words have been saved to {output_file}"
    )  # Use tqdm.write for the final message as well.


# Example usage
file_path = r"C:\Users\David\Projects\smart-drone-vision\dirty_classes.txt"
output_file = "cleaned_classes.txt"  # Name of the file to save the filtered words
filter_order = "Pinales"  # Specify the order you're interested in
filter_words_by_order(file_path, filter_order, output_file)
