from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__,template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # API call to Hugging Face model
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}  # Replace with your Hugging Face API token
        
        # Get the input text and word limit from the request
        data = request.json.get('text')
        word_limit = int(request.json.get('wordLimit', 150))  # Default to 150 if not provided

        # Function to query Hugging Face API
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        # Query the model with the input text and word limit
        output = query({
            "inputs": data,
            "parameters": {
                "max_length": word_limit,
                "min_length": 50  # Optional: you can adjust this if needed
            }
        })

        # Extract the summarized text
        summary = output[0].get('summary_text', 'Error: Unable to summarize the text.')

        # Return the summary in a JSON response
        return jsonify({'summary': summary})

    # Render the index.html page for GET requests
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
