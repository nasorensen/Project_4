from flask import Flask, render_template, request, jsonify
from model import predict_price, find_similar_homes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    beds = float(data.get("beds"))
    baths = float(data.get("baths"))
    sqft = float(data.get("sqft"))
    
    # Use 'lot_sqft' if present, else fallback to 'lot'
    lot_sqft = data.get("lot_sqft") or data.get("lot")
    if lot_sqft is None:
        return jsonify({"error": "Missing lot_sqft/lot"}), 400
    lot_sqft = float(lot_sqft)

    beds_baths_ratio = beds / baths if baths else 0
    lot_to_sqft_ratio = lot_sqft / sqft if sqft else 0

    price = predict_price(beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio)
    return jsonify({"predicted_price": price})

@app.route("/similar-homes", methods=["POST"])
def similar_homes():
    data = request.get_json()
    try:
        beds = float(data.get("beds"))
        baths = float(data.get("baths"))
        sqft = float(data.get("sqft"))
        lot_sqft = data.get("lot_sqft") or data.get("lot")
        if lot_sqft is None:
            raise ValueError("Missing lot_sqft/lot")
        lot_sqft = float(lot_sqft)

        beds_baths_ratio = beds / baths if baths else 0
        lot_to_sqft_ratio = lot_sqft / sqft if sqft else 0

    except (TypeError, ValueError) as e:
        print("Invalid input for similarity search:", data, "Error:", e)
        return jsonify([])

    similar = find_similar_homes(beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio)
    return jsonify(similar)

if __name__ == "__main__":
    app.run(debug=True)