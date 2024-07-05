from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

links = []

@app.route('/store_link', methods=['POST'])
def store_link():
    try:
        data = request.json
    except Exception as e:
        return jsonify({"message": "Invalid JSON"}), 400

    link = data.get('link')
    if not link:
        return jsonify({"message": "No link provided"}), 400

    parsed_url = urlparse(link)
    if parsed_url.scheme not in ['http', 'https']:  # Basic URL validation
        return jsonify({"message": "Invalid URL"}), 400

    if link not in links:
        links.append(link)
        # Process the link to extract product information
        # This is a sample response, replace it with actual data extraction logic
        product_info = {
            "title": "Sample Product",
            "description": "This is a sample product description.",
            "price": "$19.99",
            "rating": "4.5/5"
        }
        return jsonify(product_info), 200
    else:
        # Return existing product information if link already processed
        return jsonify({"message": "Link already exists"}), 200

@app.route('/get_links', methods=['GET'])
def get_links():
    return jsonify({"links": links}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
