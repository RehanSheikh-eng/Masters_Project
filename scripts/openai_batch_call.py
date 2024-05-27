import base64
import os
from PIL import Image
from openai import OpenAI
import json
import time
import requests
import random

def encode_image(image_path, size=(512, 512)):
    with Image.open(image_path) as img:
        img = img.resize(size)
        img_format = "PNG" if image_path.endswith(".png") else "JPEG"
        temp_filename = f"temp_image.{img_format.lower()}"
        try:
            with open(temp_filename, "wb") as temp_file:
                img.save(temp_file, format=img_format)
            with open(temp_filename, "rb") as temp_file:
                return base64.b64encode(temp_file.read()).decode('utf-8')
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

def prepare_batch_files(image_pairs, batch_folder, prompt, max_batch_size=95 * 1024 * 1024):
    os.makedirs(batch_folder, exist_ok=True)
    batch_index = 1
    current_batch_path = os.path.join(batch_folder, f"batch_input_{batch_index}.jsonl")
    current_batch_size = 0
    
    with open(current_batch_path, 'w') as batch_file:
        for i, (original_img, sam_img) in enumerate(image_pairs):
            request = {
                "custom_id": f"request-{i}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(original_img)}"}},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(sam_img)}"}}
                            ]
                        }
                    ],
                    "max_tokens": 300
                }
            }
            request_json = json.dumps(request) + '\n'
            request_size = len(request_json.encode('utf-8'))
            
            if current_batch_size + request_size > max_batch_size:
                # Start a new batch file
                batch_index += 1
                current_batch_path = os.path.join(batch_folder, f"batch_input_{batch_index}.jsonl")
                current_batch_size = 0
            
            # Write to the current batch file
            with open(current_batch_path, 'a') as batch_file:
                batch_file.write(request_json)
                current_batch_size += request_size


def prepare_batch_file_random(image_pairs, batch_file_path, prompt):
    with open(batch_file_path, 'w') as batch_file:
        for original_img, sam_img in image_pairs:
            image_id = os.path.splitext(os.path.basename(original_img))[0]
            request = {
                "custom_id": f"request-{image_id}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": "gpt-4-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(original_img)}"}},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(sam_img)}"}}
                            ]
                        }
                    ],
                    "max_tokens": 300
                }
            }
            request_json = json.dumps(request) + '\n'
            batch_file.write(request_json)


def generate_image_pairs(original_folder, processed_folder):
    original_files = sorted(os.listdir(original_folder))
    processed_files = sorted(os.listdir(processed_folder))
    
    # Assuming both folders contain exactly 2100 files in the correct order
    paths = [(os.path.join(original_folder, orig), os.path.join(processed_folder, proc))
            for orig, proc in zip(original_files, processed_files)]

    return paths


PROMPT = """
Here are two remote-sensing images, the first one is the original image and the second one is the image but  I have labelled a bright numeric ID at the centre for each visual object in the image and added colour-coded boundaries to the edges of labelled objects. Output a JSON list of captions

Make sure to follow the following instructions:
1. Describe all the important parts of the remote sensing image.
2. Do not start the sentences with “There is” when there is more than one object in an image.
3. Do not use the vague concept of words like large, tall, or many, in the absence of contrast.
4. Do not use direction nouns, such as north, south, east and west.
5. Do not refer directly to coloured boundaries in the image as they are annotations.
"""


# Paths to your folders
original_folder_path = r"C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\assets\UCM\UCM_captions\UCM_captions\imgs"
processed_folder_path = r"C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\assets\UCM\UCM_captions\UCM_captions\points_per_side=64_points_per_batch=256_pred_iou_thresh=0.85_min_mask_region_area=100_text_scale=0.3_text_thickness=1_text_padding=3_MIN_AREA_PERCENTAGE=0.007_MAX_AREA_PERCENTAGE=1"

# Generate the list of image pairs
image_pairs = generate_image_pairs(original_folder_path, processed_folder_path)
print("Prepared image pairs")

# Randomly select 10 image pairs
random_image_pairs = random.sample(image_pairs, 10)

# Prepare batch file
batch_file_path = "batch_files/batch_input.jsonl"
prepare_batch_file_random(random_image_pairs, batch_file_path, PROMPT)
print("Created batch input file:", batch_file_path)