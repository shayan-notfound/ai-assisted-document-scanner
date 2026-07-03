import os
from flask import Flask, request, render_template, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize the Gemini Client (it automatically looks for the GEMINI_API_KEY environment variable)
client = genai.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_document():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400
        
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read the uploaded image bytes
        image_bytes = file.read()
        
        # Prepare the image data structure for the SDK
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=file.mimetype
        )
        
        # Ask Gemini to extract text and clean it up
        prompt = "Extract all text from this document image. Clean up any bad formatting, fix alignments, and return it as beautifully organized readable text."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image_part]
        )
        
        return jsonify({'text': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use port 5000 by default
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
