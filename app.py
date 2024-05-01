from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from marshmallow import Schema, fields, ValidationError
import datetime
import logging


# Load environment variables
load_dotenv()


# Set your API key here
openai.api_key = 'sk-proj-sycMsoNwuEFkKMP47aLET3BlbkFJwnmvLki764XYO2RSWPzV'
if not openai.api_key:
    raise ValueError("API key is not set. Check your .env file.")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)  # Set to DEBUG for detailed logging


# Schema for incoming request data validation
class PostRequestSchema(Schema):
    rss_url = fields.Str(required=False)
    post_style = fields.Str(load_default="Inspirational")
    tone = fields.Str(load_default="Optimistic and Visionary")
    personality = fields.List(fields.Str(), load_default=["Entrepreneurial", "Empowering"])
    content_theme = fields.Str(load_default="Property Tokenization")
    schedule = fields.Dict(load_default=lambda: {'time': datetime.datetime.now().isoformat(), 'frequency': 'weekly'})

# Main page route
@app.route('/')
def home():
    return '''
    <h1>Ricardo C. Johnson LinkedIn Assistant API</h1>
    <p>Welcome to Ricardo C. Johnson's LinkedIn Content Assistant. This API is designed to generate tailored LinkedIn posts based on specific topics related to property tech and real estate.</p>
    <p><strong>Usage:</strong></p>
    <ul>
        <li>Send a POST request to /generate-post with JSON data including 'topic', 'style', 'personalize', etc.</li>
        <li>For example, {'topic': 'smart home technology', 'style': 'engaging', 'personalize': true}</li>
    </ul>
    <p>This API ensures user data privacy and adheres to all relevant security standards.</p>
    '''

# Endpoint for generating posts
@app.route('/generate-post', methods=['POST'])
def generate_post():
    try:
        data = PostRequestSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"status": "error", "message": "Invalid input data", "errors": err.messages}), 400

    content = themes_content.get(data['content_theme'], "No content available for this theme.")
    post_content = f"{content} Style: {data['post_style']}, Tone: {data['tone']}, Traits: {' & '.join(data['personality'])}."
    scheduled_time = data['schedule']['time']

    return jsonify({
        "status": "success",
        "post_content": post_content,
        "scheduled_time": scheduled_time
    }), 200

# Error handling for not found and server errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error. Please contact support.",
        "fallback_themes": ["Property Tech", "Crypto in Property", "Property Business"]
    }), 500

if __name__ == '__main__':
    # Set debug mode from an environment variable or default to False if not set
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)