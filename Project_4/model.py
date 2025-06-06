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
homes_df = pd.read_csv(HOMES_PATH, na_values=["", " "])
homes_df[["beds", "baths", "sqft", "lot_sqft"]] = homes_df[["beds", "baths", "sqft", "lot_sqft"]].apply(pd.to_numeric, errors='coerce')

def predict_price(beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio):
    # Create DataFrame with correct feature names expected by the model
    feature_names = ["beds", "baths", "sqft", "lot_sqft", "beds_baths_ratio", "lot_to_sqft_ratio"]
    features_df = pd.DataFrame([[beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio]], columns=feature_names)
    
    predicted_price = model.predict(features_df)[0]
    return round(predicted_price)

def find_similar_homes(beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio, top_n=30):
    input_vec = np.array([beds, baths, sqft, lot_sqft, beds_baths_ratio, lot_to_sqft_ratio], dtype=float)

    if np.any(pd.isnull(input_vec)) or any(x is None for x in input_vec):
        print("Skipping similarity calculation due to None or NaN in input_vec:", input_vec)
        return []

    valid_df = homes_df.dropna(subset=["beds", "baths", "sqft", "lot_sqft", "latitude", "longitude"]).copy()

    # Compute derived features for all homes
    valid_df["beds_baths_ratio"] = valid_df["beds"] / valid_df["baths"].replace(0, np.nan)
    valid_df["beds_baths_ratio"].fillna(0, inplace=True)  # handle divide by zero

    valid_df["lot_to_sqft_ratio"] = valid_df["lot_sqft"] / valid_df["sqft"].replace(0, np.nan)
    valid_df["lot_to_sqft_ratio"].fillna(0, inplace=True)

    feature_matrix = valid_df[["beds", "baths", "sqft", "lot_sqft", "beds_baths_ratio", "lot_to_sqft_ratio"]].to_numpy(dtype=float)

    distances = np.linalg.norm(feature_matrix - input_vec, axis=1)
    valid_df["similarity"] = distances

    similar = valid_df.nsmallest(top_n, "similarity")

    return similar[[
    "latitude",
    "longitude",
    "sold_price",
    "beds",
    "baths",
    "sqft",
    "lot_sqft",
    "street",
    "city",
    "zip"
]].to_dict(orient="records")