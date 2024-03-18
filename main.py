from flask import Flask, request, jsonify
import requests
import io
from PIL import Image
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")
AUTHORIZATION_TOKEN = os.environ.get("AUTHORIZATION_TOKEN")

def query(payload):
    try:
        headers = {"Authorization": f"Bearer {AUTHORIZATION_TOKEN}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.content
    except requests.exceptions.RequestException as e:
        return None

def upload_image_to_imgbb(image_bytes):
    try:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY, "expiration": "never"}, 
            files={"image": image_bytes},
        )
        response.raise_for_status()
        return response.json()["data"]["url"]
    except requests.exceptions.RequestException as e:
        return None

@app.route('/prompt', methods=['POST'])
def process_prompt():
    prompt = request.form.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    image_bytes = query({"inputs": prompt})

    if image_bytes:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.save("img.jpg")

            with open("img.jpg", "rb") as f:
                image_bytes = f.read()  # Read the image bytes

            imgbb_url = upload_image_to_imgbb(image_bytes)
            if imgbb_url:
                return jsonify({'image_url': imgbb_url}), 200
            else:
                return jsonify({'error': 'Failed to upload image to imgBB'}), 500
        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Failed to retrieve image'}), 500

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0' , port=8080)
