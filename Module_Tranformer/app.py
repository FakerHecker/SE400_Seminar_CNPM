from flask import Flask, request, jsonify, render_template
from src.predict import ToxicPredictor
import os

app = Flask(__name__)

# Load model ONCE when app starts
print("Initializing Model for API...")
predictor = ToxicPredictor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
            
        # Run prediction
        result = predictor.predict(text)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Chạy server
    print("Server running at http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False) 
    # use_reloader=False để tránh load model 2 lần