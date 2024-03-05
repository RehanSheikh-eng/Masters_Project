# tests/test_routes.py
import os
import unittest
from unittest.mock import patch
from flask import current_app, json
from werkzeug.datastructures import FileStorage
from app import create_app
from PIL import Image
import numpy as np


class ComputeEmbeddingRouteTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by creating the app with testing configuration 
        and setting up the test client.
        """
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
    
    def test_compute_embedding_success(self):
        with self.app.app_context():

            # Generate a test image with random pixels
            image_size = (50, 50)
            image_array = np.random.rand(*image_size, 3) * 255
            test_image = Image.fromarray(image_array.astype('uint8')).convert('RGB')


            test_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'test_image.jpg')
            test_image.save(test_image_path)

            with open(test_image_path, 'rb') as f:
                test_file = FileStorage(
                    stream=f,
                    filename='test_image.jpg',
                    content_type='image/jpeg',
                )
            
                data = {
                    'file': test_file
                }
            
                # Send POST request to the endpoint
                response = self.client.post('/api/compute_embedding', data=data, content_type='multipart/form-data')
                
            self.assertEqual(response.status_code, 200)
            self.assertIn('embedding', response.json)
            self.assertTrue(response.json['success'])
            self.assertFalse(os.path.exists(test_image_path), "The file should have been deleted by the endpoint but still exists.")


    def test_compute_embedding_no_file(self):
        response = self.client.post('/api/compute_embedding', data={})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json['success'])
        self.assertIn('error', response.json)


class GPT4VEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

    @patch('openai.OpenAI.completions.create')
    def test_upload_gpt4v_success(self, mock_openai):
        # Mock the OpenAI response
        mock_openai.return_value = {
            "choices": [{"message": {"content": "Mocked OpenAI response"}}]
        }

        # Prepare the data for your POST request
        data = {
            "file": "data:image/png;base64,....",  # Your base64 image string here
            "prompt": "Describe this image.",
            "max_tokens": 1000
        }

        response = self.client.post('/api/upload_gpt4v', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertIn('Mocked OpenAI response', response.json['analysis'])



if __name__ == '__main__':
    unittest.main()
