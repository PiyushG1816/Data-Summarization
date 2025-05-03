from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    # API call to Hugging Face model
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN')}"}

    # Get input text and word limit from request JSON
    data = request.json.get('text')
    word_limit = int(request.json.get('wordLimit', 150))

    if not data:
        return jsonify({"error": "Missing 'text' in request"}), 400

    # Call the Hugging Face API
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": data,
        "parameters": {
            "max_length": word_limit,
            "min_length": 50
        }
    })

    summary = output[0].get('summary_text', 'Error: Unable to summarize the text.')

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
