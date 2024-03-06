import os
import sys
import time
from sklearn.model_selection import KFold

def display_signature_progress():
    bar_slots = "🍒🍋🔔💰🚁🛩️🛸🚀🛰️"
    drone_str = "DRONE2MAX!"
    bar_width = len(drone_str)

    for i in range(101):
        letter_index = i // 10
        bar_str = drone_str[:letter_index] + bar_slots[((i % 10) - 1) % len(bar_slots)] * (bar_width - letter_index)
        bar_str = bar_str[:bar_width]

        sys.stdout.write(f'\r[{bar_str}] {i}%')
        sys.stdout.flush()
        time.sleep(0.05)

def get_dataset_files(images_dir, labels_dir):
    image_files = [
        (os.path.join(dirpath, filename), os.path.join(labels_dir, dirpath.split(os.path.sep)[-1], filename.replace('.jpg', '.txt')))
        for dirpath, _, filenames in os.walk(images_dir)
        for filename in filenames
        if filename.endswith(".jpg") and os.path.exists(os.path.join(labels_dir, dirpath.split(os.path.sep)[-1], filename.replace('.jpg', '.txt')))
    ]
    return image_files

images_dir = "C:/Users/David/Projects/smart-drone-vision/Dataset/dataset/images"
labels_dir = "C:/Users/David/Projects/smart-drone-vision/Dataset/dataset/labels"

dataset_files = get_dataset_files(images_dir, labels_dir)

num_folds = 5
kf = KFold(n_splits=num_folds, shuffle=True, random_state=42)

for fold, (train_index, val_index) in enumerate(kf.split(dataset_files)):
    print(f"\n\nPreparing data for Fold {fold+1}")
    display_signature_progress()
    
    train, val = [dataset_files[i] for i in train_index], [dataset_files[i] for i in val_index]
    
    print(f"\nFold {fold+1} prepared. Train examples: {len(train)}, Validation examples: {len(val)}")