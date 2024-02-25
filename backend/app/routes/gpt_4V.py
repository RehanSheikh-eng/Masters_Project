from flask import Blueprint, request, jsonify, current_app
from openai import OpenAI
import os
import base64
from werkzeug.utils import secure_filename

gpt_4v_bp = Blueprint('gpt_4v', __name__, url_prefix='/api')

@gpt_4v_bp.route('/upload_gpt4v', methods=['POST'])
def process_image():
    if current_app.config['DEBUG']:
        current_app.logger.debug('Starting the image processing API call')

    # Initialize variables
    base64_image = None
    customPrompt = request.form.get('prompt', "Describe this image in detail.")
    detail = request.form.get('detail', '')
    max_tokens = request.form.get('max_tokens', 1000)

    # Check if a file part exists in the request
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        # Convert the file read to base64
        base64_image = base64.b64encode(file.read()).decode('utf-8')
        if current_app.config['DEBUG']:
            current_app.logger.debug('File uploaded and converted to base64')

    # Fallback to base64 image string provided in JSON body if no file was uploaded
    elif request.json and 'file' in request.json:
        base64_image = request.json['file']
        if current_app.config['DEBUG']:
            current_app.logger.debug('Received image in base64 format from JSON')

    if not base64_image:
        error_msg = 'No image provided'
        if current_app.config['DEBUG']:
            current_app.logger.debug(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 400

    if current_app.config['DEBUG']:
        current_app.logger.debug(f'Using prompt: {customPrompt}')

    try:

        # Configure OpenAI API Key
        client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # this is also the default, it can be omitted
        )
        # openai.api_key = current_app.config.get('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')

        if current_app.config['DEBUG']:
            current_app.logger.debug('Sending request to OpenAI')

        # Prepare and send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                "role": "user",
                "content": [
                        {
                            "type": "text",
                            "text": customPrompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                        }
                    ]
                }
            ],
            max_tokens=int(max_tokens)
        )

        if current_app.config['DEBUG']:
            current_app.logger.debug('Received response from OpenAI')

        analysis = response.choices[0].message.content

        if current_app.config['DEBUG']:
            current_app.logger.debug(f'Analysis: {analysis}')

        return jsonify({'success': True, 'analysis': analysis})

    except Exception as e:
        error_msg = f'Error sending request to OpenAI: {e}'
        if current_app.config['DEBUG']:
            current_app.logger.error(error_msg)
        return jsonify({'success': False, 'message': 'Failed to process image with OpenAI'}), 500
