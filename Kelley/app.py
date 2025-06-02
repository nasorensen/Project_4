from flask import Flask, render_template, request, flash
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "your_secret_key"  # Needed for flashing messages

# Load and preprocess data
try:
    df = pd.read_csv("kingcountysales_2020_2023 (1).csv")
except FileNotFoundError:
    raise Exception("CSV file not found. Please check the file path.")

columns = ['sale_price', 'sqft', 'beds', 'bath_full', 'latitude', 'longitude']
df = df[columns].dropna().copy()  # Use .copy() to avoid SettingWithCopyWarning

# Normalize data
features = ['sqft', 'beds', 'bath_full']
scaler = MinMaxScaler()
X = scaler.fit_transform(df[features])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            sqft = int(request.form["sqft"])
            beds = int(request.form["beds"])
            bath_full = int(request.form["bath_full"])
        except (ValueError, KeyError):
            flash("Please enter valid numbers for all fields.")
            return render_template("index.html", map_generated=False)

        user_input = {
            "sqft": sqft,
            "beds": beds,
            "bath_full": bath_full
        }

        # Compute similarity scores
        user_vector = scaler.transform([[user_input[f] for f in features]])
        df["similarity"] = cosine_similarity(user_vector, X)[0]

        # Create Folium Map
        m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=10)
        cluster = MarkerCluster().add_to(m)

        #Filter similar homes (similarity > 0.9)
        similar_homes = df[df["similarity"] > 0.9]

        # Add markers
        for _, row in similar_homes.iterrows():
            popup = f"""
            <div style="font-family: Arial; font-size: 14px; color: black;">
                <b>Price:</b> <span style="color: green;">${row['sale_price']:,.0f}</span><br>
                <b>Sqft:</b> {row['sqft']}<br>
                <b>Beds:</b> {row['beds']}<br>
                <b>Baths:</b> {row['bath_full']}<br>
                <b>Similarity Score:</b> <span style="color: green;">{row['similarity']:.2f}</span>
            </div>
            """
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color="green",
                fill=True,
                fill_color="green",
                fill_opacity=0.7,
                popup=folium.Popup(popup, max_width=300)
            ).add_to(cluster)

        # Ensure static directory exists
        os.makedirs("static", exist_ok=True)
        m.save("static/map.html")
        print("map saved successfully")
        return render_template("index.html", map_generated=True)

    return render_template("index.html", map_generated=False)

if __name__ == "__main__":
    app.run(debug=True)