# routes/gpt_4V.py
from flask import Blueprint, request, jsonify, current_app
import openai
import os

# Initialize your Flask Blueprint
gpt_4v_bp = Blueprint('gpt_4v', __name__, url_prefix='/api')

@gpt_4v_bp.route('/upload_gpt4v', methods=['POST'])
def process_image():
    # Check if debug mode is enabled
    if current_app.config['DEBUG']:
        current_app.logger.debug('Starting the image processing API call')

    data = request.json
    base64Image = data.get('file')
    customPrompt = data.get('prompt', "Describe this image in detail.")
    detail = data.get('detail', '')
    max_tokens = data.get('max_tokens', 1000)

    if not base64Image:
        error_msg = 'No file found in the request'
        if current_app.config['DEBUG']:
            current_app.logger.debug(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 400

    if current_app.config['DEBUG']:
        current_app.logger.debug('Received image in base64 format')

    if current_app.config['DEBUG']:
        current_app.logger.debug(f'Using prompt: {customPrompt}')

    try:
        # Configure OpenAI API Key
        openai.api_key = current_app.config.get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')

        # Sending the image and prompt to OpenAI for processing
        if current_app.config['DEBUG']:
            current_app.logger.debug('Sending request to OpenAI')

        # Prepare and send request to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": customPrompt,
                    "image_base64": base64Image,
                    **({'detail': detail} if detail else {})
                }
            ],
            max_tokens=max_tokens
        )        
        
        if current_app.config['DEBUG']:
            current_app.logger.debug('Received response from OpenAI')

        # Process and return the response
        analysis = response.choices[0].message.content

        if current_app.config['DEBUG']:
            current_app.logger.debug(f'Analysis: {analysis}')
        
        return jsonify({'success': True, 'analysis': analysis})

    except Exception as e:
        error_msg = f'Error sending request to OpenAI: {e}'
        if current_app.config['DEBUG']:
            current_app.logger.error(error_msg)
        return jsonify({'success': False, 'message': 'Failed to process image with OpenAI'}), 500


