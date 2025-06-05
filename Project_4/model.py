import joblib
import os
import pandas as pd
import numpy as np

# Load the model once when the app starts
MODEL_PATH = os.path.join("data", "sold_price_model.pkl")
model = joblib.load(MODEL_PATH)

# Load CSV for similar homes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOMES_PATH = os.path.join(BASE_DIR, "data", "st_paul_sold_properties.csv")
homes_df = pd.read_csv(HOMES_PATH)
homes_df = pd.read_csv(HOMES_PATH, na_values=["", " "])
homes_df[["beds", "baths", "sqft", "lot_sqft"]] = homes_df[["beds", "baths", "sqft", "lot_sqft"]].apply(pd.to_numeric, errors='coerce')

def predict_price(beds, baths, sqft, lot):
    features = [[beds, baths, sqft, lot]]
    predicted_price = model.predict(features)[0]
    return round(predicted_price)

def find_similar_homes(beds, baths, sqft, lot, top_n=10):
    input_vec = np.array([beds, baths, sqft, lot], dtype=float)

    # Skip if any input is invalid
    if np.any(pd.isnull(input_vec)) or any(x is None for x in input_vec):
        print("Skipping similarity calculation due to None or NaN in input_vec:", input_vec)
        return []

    # Drop rows missing any required features
    valid_df = homes_df.dropna(subset=["beds", "baths", "sqft", "lot_sqft", "latitude", "longitude"]).copy()

    # Matrix of home features
    feature_matrix = valid_df[["beds", "baths", "sqft", "lot_sqft"]].to_numpy(dtype=float)

    # Vectorized distance calculation
    distances = np.linalg.norm(feature_matrix - input_vec, axis=1)
    valid_df["similarity"] = distances

    # Select top N most similar homes
    similar = valid_df.nsmallest(top_n, "similarity")

    return similar[["latitude", "longitude", "sold_price"]].to_dict(orient="records")