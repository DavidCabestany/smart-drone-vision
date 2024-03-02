import os
import shutil
import random
import re

def prepare_images_for_annotation(source_dir, test_dir, images_to_keep=6):
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    def contains_special_characters(filename):
        return not re.match(r'^[\w\-]+\.[\w\-]+$', filename)

    def move_images_with_special_chars():
        for image in os.listdir(source_dir):
            if contains_special_characters(image):
                shutil.move(os.path.join(source_dir, image), os.path.join(test_dir, image))

    def select_and_move_images():
        folder_images = {}
        for image in os.listdir(source_dir):
            original_folder_name = "_".join(image.split('_')[:-1])
            folder_images.setdefault(original_folder_name, []).append(image)

        for images in folder_images.values():
            if len(images) > images_to_keep:
                images_to_move = set(images) - set(random.sample(images, images_to_keep))
                for image in images_to_move:
                    shutil.move(os.path.join(source_dir, image), os.path.join(test_dir, image))

    move_images_with_special_chars()
    select_and_move_images()

def clean_up_after_annotation(source_dir, annotation_dir, test_dir):
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    for image_file in os.listdir(source_dir):
        annotation_file = os.path.splitext(image_file)[0] + '.txt'
        if not os.path.exists(os.path.join(annotation_dir, annotation_file)):
            shutil.move(os.path.join(source_dir, image_file), os.path.join(test_dir, image_file))



# Uncomment to Prepare Images for Annotation
source_dir = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\images'
test_dir = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\test'
# prepare_images_for_annotation(source_dir, test_dir) 

# Uncomment to Clean Up after Annotation
annotation_dir = r'C:\Users\David\Projects\smart-drone-vision\Dataset\Pinopsida\labels'
clean_up_after_annotation(source_dir, annotation_dir, test_dir)
