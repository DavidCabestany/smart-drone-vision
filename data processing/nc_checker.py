import os

def check_annotations(labels_path, nc=67):
    """
    Check all annotation files in the given directory to ensure that class labels are within the expected range.

    :param labels_path: Path to the directory containing YOLO format annotation files.
    :param nc: Number of classes. Class labels should range from 0 to nc-1.
    """
    out_of_range_labels = []
    for filename in os.listdir(labels_path):
        if filename.endswith(".txt") and not filename.startswith("classes"):
            with open(os.path.join(labels_path, filename), 'r') as file:
                for line in file:
                    class_id = int(line.split()[0])  # Class ID is the first value in each line
                    if class_id < 0 or class_id >= nc:
                        out_of_range_labels.append((filename, class_id))

    if out_of_range_labels:
        print(f"Found labels out of range in {len(out_of_range_labels)} annotation files:")
        for filename, class_id in out_of_range_labels:
            print(f"  {filename}: {class_id}")
    else:
        print("All labels are within the expected range.")

# Example usage
labels_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\labels'  # Update this path
check_annotations(labels_path, nc=67)


# Let's assume labels_path is the directory containing the annotation files

nc = 66  # Number of classes, adjust according to your dataset

# Set the path to your annotation files
labels_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\labels'  # Update this path


# Initialize lists to hold out-of-range labels and invalid files
out_of_range_labels = []
invalid_files = []

# Scanning through all .txt annotation files in the labels_path
for filename in os.listdir(labels_path):
    file_path = os.path.join(labels_path, filename)
    if filename.endswith(".txt") and not filename.startswith("classes"):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    class_id = int(line.split()[0])  # Extracting class ID from each line
                    if class_id < 0 or class_id >= nc:  # Checking if class ID is out of expected range
                        out_of_range_labels.append((filename, class_id))
                except ValueError:
                    # Catching files with unexpected content that might not represent a class ID
                    invalid_files.append(filename)

# Print out-of-range labels and invalid files
print("Out of Range Labels:", out_of_range_labels)
print("Invalid Files:", invalid_files)


def check_annotations_and_print_classes(labels_path, nc=67):
    """
    Check all annotation files in the given directory to ensure that class labels are within the expected range.
    Also, print all unique class indices found in the annotation files.

    :param labels_path: Path to the directory containing YOLO format annotation files.
    :param nc: Number of classes. Class labels should range from 0 to nc-1.
    """
    out_of_range_labels = []
    all_class_indices = set()  # Set to store all unique class indices

    for filename in os.listdir(labels_path):
        if filename.endswith(".txt") and not filename.startswith("classes"):
            with open(os.path.join(labels_path, filename), 'r') as file:
                for line in file:
                    try:
                        class_id = int(line.split()[0])  # Extracting class ID from each line
                        all_class_indices.add(class_id)  # Add class ID to set of all indices
                        if class_id < 0 or class_id >= nc:  # Checking if class ID is out of expected range
                            out_of_range_labels.append((filename, class_id))
                    except ValueError:
                        # This line does not start with a class ID, ignore it
                        continue

    if out_of_range_labels:
        print(f"Found labels out of range in {len(out_of_range_labels)} annotation files:")
        for filename, class_id in out_of_range_labels:
            print(f"  {filename}: {class_id}")
    else:
        print("All labels are within the expected range.")
    
    # Print all unique class indices found
    print("\nUnique class indices found in annotation files:", sorted(all_class_indices))

names = ['Abies', 'Acmopyle', 'Actinostrobus', 'Afrocarpus', 'Amentotaxus', 'Araucaria', 'Athrotaxis', 'Austrocedrus', 'Austrotaxus', 'Callitris', 'Calocedrus', 'Cathaya', 'Cephalotaxus', 'Chamaecyparis', 'Cupressinoxylon', 'Cupressus', 'Dacrycarpus', 'Dadoxylon', 'Diselma', 'Doliostrobus', 'Fitzroya', 'Glyptostrobus', 'Halocarpus', 'Juniperus', 'Keteleeria', 'Lagarostrobos', 'Larix', 'Lepidothamnus', 'Libocedrus', 'Manoao', 'Mesocyparis', 'Metasequoia', 'Microbiota', 'Microcachrys', 'Nageia', 'Neocallitropsis', 'Pagiophyllum', 'Pararaucaria', 'Parasitaxus', 'Pherosphaera', 'Phyllocladus', 'Picea', 'Pilgerodendron', 'Pinites', 'Platycladus', 'Podocarpus', 'Prumnopitys', 'Pseudolarix', 'Pseudotsuga', 'Quasisequoia', 'Retrophyllum', 'Saxegothaea', 'Sciadopitys', 'Sequoia', 'Sequoiadendron', 'Sundacarpus', 'Taxodioxylon', 'Taxodium', 'Taxus', 'Tetraclinis', 'Thuja', 'Thujopsis', 'Tsuga', 'Widdringtonia', 'Wollemia', 'Pinus']


namesw = [
    "Abies",
    "Acmopyle",
    "Actinostrobus",
    "Afrocarpus",
    "Amentotaxus",
    "Araucaria",
    "Athrotaxis",
    "Austrocedrus",
    "Austrotaxus",
    "Callitris",
    "Calocedrus",
    "Cathaya",
    "Cephalotaxus",
    "Chamaecyparis",
    "Cupressinoxylon",
    "Cupressus",
    "Dacrycarpus",
    "Dadoxylon",
    "Diselma",
    "Doliostrobus",
    "Fitzroya",
    "Glyptostrobus",
    "Halocarpus",
    "Juniperus",
    "Keteleeria",
    "Lagarostrobos",
    "Larix",
    "Lepidothamnus",
    "Libocedrus",
    "Manoao",
    "Mesocyparis",
    "Metasequoia",
    "Microbiota",
    "Microcachrys",
    "Nageia",
    "Neocallitropsis",
    "Pagiophyllum",
    "Pararaucaria",
    "Parasitaxus",
    "Pherosphaera",
    "Phyllocladus",
    "Picea",
    "Pilgerodendron",
    "Pinites",
    "Platycladus",
    "Podocarpus",
    "Prumnopitys",
    "Pseudolarix",
    "Pseudotsuga",
    "Quasisequoia",
    "Retrophyllum",
    "Saxegothaea",
    "Sciadopitys",
    "Sequoia",
    "Sequoiadendron",
    "Sundacarpus",
    "Taxodioxylon",
    "Taxodium",
    "Taxus",
    "Tetraclinis",
    "Thuja",
    "Thujopsis",
    "Tsuga",
    "Widdringtonia",
    "Wollemia",
    "Pinus"
]

print([i for i in range(len(names))])
print([i for i in range(len(namesw))])
# Example usage
labels_path = r'C:\Users\David\Projects\smart-drone-vision\Dataset\labels'  # Update this path
check_annotations_and_print_classes(labels_path, nc=67)
