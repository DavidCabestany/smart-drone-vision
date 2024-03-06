import os
import numpy as np
from sklearn.model_selection import KFold
import time
import sys

# Your signature progress bar implementation
def display_signature_progress():
    # Define your custom bar sequence
    bar_slots = "🍒🍋🔔💰🚁🛩️🛸🚀🛰️"
    drone_str = "DRONE2MAX!"
    bar_width = len(drone_str)

    # Simulate progress
    for i in range(101):
        # Determine the index of the next letter to reveal
        letter_index = i // 10
        # Create the bar string with emojis and the portion of the DRONE2MAX string revealed
        bar_str = drone_str[:letter_index] + bar_slots[((i % 10) - 1) % len(bar_slots)] * (bar_width - letter_index)
        # Ensure the bar string isn't longer than the bar width
        bar_str = bar_str[:bar_width]

        # Print the progress bar
        sys.stdout.write(f'\r[{bar_str}] {i}%')
        sys.stdout.flush()

        # Simulate some work
        time.sleep(0.05)  # Reduced sleep time for quicker demonstration

def get_dataset_files(images_dir, labels_dir):
    image_files = []
    for dirpath, _, filenames in os.walk(images_dir):
        for filename in filenames:
            if filename.endswith(".jpg"):  # Assuming JPEG format; adjust as necessary
                image_path = os.path.join(dirpath, filename)
                label_path = os.path.join(labels_dir, dirpath.split(os.path.sep)[-1], filename.replace('.jpg', '.txt'))
                if os.path.exists(label_path):  # Ensure corresponding label exists
                    image_files.append((image_path, label_path))
    return image_files

# Paths to your images and labels directories
images_dir = "C:/Users/David/Projects/smart-drone-vision/Dataset/dataset/images"
labels_dir = "C:/Users/David/Projects/smart-drone-vision/Dataset/dataset/labels"

# Combine training and validation sets
dataset_files = get_dataset_files(images_dir, labels_dir)

# Define the KFold cross-validator
num_folds = 5
kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)

# Split dataset into K folds
for fold, (train_index, val_index) in enumerate(kf.split(dataset_files)):
    print(f"\n\nPreparing data for Fold {fold+1}")
    display_signature_progress()  # Display the signature progress bar for each fold
    
    train, val = [dataset_files[i] for i in train_index], [dataset_files[i] for i in val_index]
    
    # Here, you'd handle saving or processing of this fold's data
    print(f"\nFold {fold+1} prepared. Train examples: {len(train)}, Validation examples: {len(val)}")
    # Additional logic to save the fold data for training/validation could go here
