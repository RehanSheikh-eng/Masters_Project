from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from segment_anything import sam_model_registry, SamPredictor
import numpy as np
import cv2
import os
import torch
import openai

app = Flask(__name__)

# Temporary directory to save uploaded files
UPLOAD_FOLDER = r'C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\backend\temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variable to hold the model
model = None

# Initialize OpenAI client with your API key
openai.api_key = os.getenv('OPENAI_API_KEY')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/compute_embedding', methods=['POST'])
def upload_file():
    global model

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:  # Implement allowed_file to check for file format
        # Save the file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(torch.cuda.is_available())

        # Read the saved image file
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        checkpoint = r"C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\backend\sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        sam = sam_model_registry[model_type](checkpoint=checkpoint)

        if torch.cuda.is_available():
            sam.to(device='cuda')
        else:
            sam.to(device='cpu')
        model = SamPredictor(sam)
        
        model.set_image(image)

        # Compute the embedding
        image_embedding = model.get_image_embedding().cpu().numpy()

        # Optionally, delete the image file after processing
        os.remove(file_path)

        return jsonify({'embeddings': image_embedding.tolist()}), 200

    return jsonify({'error': 'Invalid file format'}), 400



@app.route('/api/upload_gpt4v', methods=['POST'])
def process_image():
    # Logging the start of the image processing API call
    print('Starting the image processing API call')

    # Extracting the file (in base64 format) and an optional custom prompt from the request body
    data = request.json
    base64Image = data.get('file')
    customPrompt = data.get('prompt')
    detail = data.get('detail')
    max_tokens = data.get('max_tokens', 1000)  # Default to 1000 if not provided

    # Check if the image file is included in the request
    if not base64Image:
        print('No file found in the request')
        return jsonify({'success': False, 'message': 'No file found'}), 400

    print('Received image in base64 format')

    # Utilize the provided custom prompt or a default one if not provided
    promptText = customPrompt or "Analyze and describe the image in detail. Focus on visual elements like colors, object details, people's positions and expressions, and the environment. Transcribe any text as 'Content: “[Text]”', noting font attributes. Aim for a clear, thorough representation of all visual and textual aspects."

    print(f'Using prompt: {promptText}')

    # Sending the image and prompt to OpenAI for processing
    print('Sending request to OpenAI')
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": promptText},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": base64Image,
                                **({'detail': detail} if detail else {})  # Include the detail field only if it exists
                            }
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )

        print('Received response from OpenAI')
        # Extract the analysis from the response
        analysis = response.choices[0].message.content
        print('Analysis:', analysis)

        # Return the analysis in the response
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        print(f'Error sending request to OpenAI: {e}')
        return jsonify({'success': False, 'message': 'Error sending request to OpenAI'}), 500



def load_model_to_memory():
    global model
    checkpoint = r"C:\Users\relic\Documents\School\Engineering_Cam\Part IIB\Masters Project\sam\segment-anything\backend\sam_vit_h_4b8939.pth"
    model_type = "vit_h"
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    sam.to(device='cuda')
    model = SamPredictor(sam)
    print(model)

if __name__ == '__main__':
    load_model_to_memory()  # Load the model into memory
    app.run(debug=True, use_reloader=False)
