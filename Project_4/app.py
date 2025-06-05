from flask import Flask, render_template, request, jsonify
from model import predict_price, find_similar_homes

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    beds = data.get("beds")
    baths = data.get("baths")
    sqft = data.get("sqft")
    lot = data.get("lot_sqft")
    print("Received data for prediction:", data)

    price = predict_price(beds, baths, sqft, lot)
    print(f"Input: {data}, Predicted Price: {price}")  # Debug logging

    # Eventually add similar homes
    return jsonify({"predicted_price": price})

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/similar-homes", methods=["POST"])
def similar_homes():
    data = request.get_json()

    try:
        beds = int(data.get("beds"))
        baths = float(data.get("baths"))
        sqft = int(data.get("sqft"))
        lot = int(data.get("lot"))  # <-- this was coming through as None
    except (TypeError, ValueError) as e:
        print("Invalid input for similarity search:", data, "Error:", e)
        return jsonify([])

    similar = find_similar_homes(beds, baths, sqft, lot)
    return jsonify(similar)