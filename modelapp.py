from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)

# Load trained model
model = pickle.load(open("Model_Selection/sold_price_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]
        return jsonify({"predicted_price": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handles errors gracefully
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)