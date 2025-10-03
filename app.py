from flask import Flask, request, jsonify
from flask_cors import CORS
from joblib import load
import re

app = Flask(__name__)
CORS(app)

# --- LOAD THE PRE-TRAINED MODELS ON STARTUP ---
# The model and vectorizer are loaded only once when the app starts.
try:
    vectorizer = load('vectorizer.pkl')
    model = load('model.pkl')
    print("Model and vectorizer loaded successfully.")
except FileNotFoundError:
    print("Error: model.pkl or vectorizer.pkl not found. Please train the model first.")
    vectorizer = None
    model = None


def clean_text(text):
    # This function must be available for the predict route
    text = re.sub(r'\W', ' ', str(text))  # Ensure text is a string
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text


@app.route('/')
def home():
    return "Spam Detector API is live and running!"


@app.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.json
    email_content = data['text']

    # Use the loaded objects to make a prediction
    cleaned_text = clean_text(email_content)
    vect_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vect_text)[0]

    # Use 'spam'/'ham' or similar string labels from your training data
    result = 'Spam' if prediction == 1 else 'Not Spam'

    # Send back a 'prediction' key to match your JavaScript
    return jsonify({'prediction': result})


if __name__ == '__main__':
    app.run(debug=True)