from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os
import torch
from segment_anything import sam_model_registry, SamPredictor
import requests
import base64
# Blueprint setup
compute_embedding_bp = Blueprint('compute_embedding', __name__, url_prefix='/api')

@compute_embedding_bp.route('/compute_embedding', methods=['POST'])
def compute_embedding():
    """
    Compute and return the embedding for an uploaded image.
    
    This endpoint expects a multipart/form-data request containing a file part named 'file'.
    The response returns a JSON object with the embedding data, its shape, and data type.

    Responses:
    200: Successfully computed the embedding.
         Returns a JSON object with 'success': true and the embedding details.
    400: Bad request, such as no file part included or no file selected.
         Returns a JSON object with 'success': false and an error message.
    """
    if current_app.config['DEBUG']:
        current_app.logger.debug('Compute embedding called.')

    # if 'application/json' not in request.headers['Content-Type']:
    #         return jsonify({'success': False, 'error': 'Invalid content type, expected application/json'}), 400

    data = request.json
    center = data.get('center')
    zoom = data.get('zoom')
    size = data.get('size')

    if not center or not zoom:
        return jsonify({'success': False, 'error': 'Missing required parameters: center and zoom'}), 400

    # Fetch the static map image
    try:
        map_image = fetch_static_map_image(center, zoom, size=size)
    except requests.RequestException as e:
        return jsonify({'success': False, 'error': 'Failed to fetch static map image'}), 500

    # Save the fetched image temporarily
    temp_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_map_image.png')
    with open(temp_image_path, 'wb') as img_file:
        img_file.write(map_image)

    if current_app.config['DEBUG']:
        current_app.logger.debug(f'File {img_file} saved to {temp_image_path}')

    # Process the image and compute the embedding
    image = cv2.imread(temp_image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    checkpoint_path = current_app.config['MODEL_CHECKPOINT_PATH']
    model_type = current_app.config['MODEL_TYPE']
    sam = sam_model_registry[model_type](checkpoint=checkpoint_path)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    sam.to(device=device)
    model = SamPredictor(sam)
    model.set_image(image)
    image_embedding = model.get_image_embedding().cpu().numpy()

    if current_app.config['DEBUG']:
        current_app.logger.debug('Embedding computation completed.')

    os.remove(temp_image_path)  # Clean up the uploaded file

    embedding_response = {
        'success': True,
        'image': base64.b64encode(map_image).decode('utf-8'),
        'embedding': {
            'data': image_embedding.flatten().tolist(),
            'shape': image_embedding.shape,
            'dtype': str(image_embedding.dtype)
        }
    }
    return jsonify(embedding_response), 200




def fetch_static_map_image(center, zoom, size="600x300", maptype="satellite", scale=2):
    """
    Fetches a static map image from the Google Maps Static API.

    Args:
        center (str): The center of the map (latitude,longitude).
        zoom (int): The zoom level of the map.
        size (str, optional): The size of the map image (widthxheight). Defaults to "600x300".
        maptype (str, optional): The type of map to construct. Defaults to "satellite".

    Returns:
        bytes: The image data of the fetched static map.
    """
    GOOGLE_MAPS_STATIC_API_KEY = current_app.config['GOOGLE_MAPS_STATIC_API_KEY']
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"

    params = {
        "center": center,
        "zoom": zoom,
        "size": size,
        "scale": scale,
        "maptype": maptype,
        "key": GOOGLE_MAPS_STATIC_API_KEY
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for bad requests

    return response.content