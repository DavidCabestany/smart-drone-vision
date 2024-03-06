import os

def check_annotations_and_print_classes(labels_path: str, nc: int = 67) -> None:
    """
    Checks all annotation files in the specified directory to ensure that class labels
    are within the expected range, and prints all unique class indices found.

    Args:
        labels_path: Path to the directory containing YOLO format annotation files.
        nc: Number of classes. Class labels should range from 0 to nc-1.
    """
    out_of_range_labels = []
    all_class_indices = set()  # Set to store all unique class indices
    invalid_files = []

    # Scanning through all .txt annotation files in the labels_path
    for filename in os.listdir(labels_path):
        if filename.endswith(".txt") and not filename.startswith("classes"):
            file_path = os.path.join(labels_path, filename)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        try:
                            class_id = int(line.split()[0])  # Extracting class ID from each line
                            all_class_indices.add(class_id)  # Add class ID to set of all indices
                            if class_id < 0 or class_id >= nc:  # Checking if class ID is out of expected range
                                out_of_range_labels.append((filename, class_id))
                        except ValueError:
                            # This line does not start with a class ID, likely invalid format
                            invalid_files.append(filename)
                            break  # No need to process further lines in this file
            except IOError as e:
                print(f"Could not read file {filename}: {e}")
                continue

    # Report findings
    if out_of_range_labels:
        print(f"Found labels out of range in {len(out_of_range_labels)} annotation files:")
        for filename, class_id in out_of_range_labels:
            print(f"  {filename}: {class_id}")
    else:
        print("All labels are within the expected range.")

    if invalid_files:
        print(f"\nInvalid files (non-YOLO format or other errors): {len(invalid_files)}")
        for filename in invalid_files:
            print(f"  {filename}")

    print("\nUnique class indices found in annotation files:", sorted(all_class_indices))

# Example usage
labels_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\labels'  # Update this path
check_annotations_and_print_classes(labels_path, nc=67)
