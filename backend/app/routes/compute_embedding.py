from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os
import torch
from segment_anything import sam_model_registry, SamPredictor

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

    if 'file' not in request.files:
        error_msg = 'No file part'
        if current_app.config['DEBUG']:
            current_app.logger.debug(f'Error: {error_msg}')
        return jsonify({'success': False, 'error': error_msg}), 400

    file = request.files['file']
    if file.filename == '':
        error_msg = 'No selected file'
        if current_app.config['DEBUG']:
            current_app.logger.debug(f'Error: {error_msg}')
        return jsonify({'success': False, 'error': error_msg}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    if current_app.config['DEBUG']:
        current_app.logger.debug(f'File {filename} saved to {file_path}')

    # Process the image and compute the embedding
    image = cv2.imread(file_path)
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

    os.remove(file_path)  # Clean up the uploaded file

    embedding_response = {
        'success': True,
        'embedding': {
            'data': image_embedding.flatten().tolist(),
            'shape': image_embedding.shape,
            'dtype': str(image_embedding.dtype)
        }
    }
    return jsonify(embedding_response), 200
