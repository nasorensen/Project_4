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
    df = pd.read_csv("resources/st_paul_sold_properties.csv")
except FileNotFoundError:
    raise Exception("CSV file not found. Please check the file path.")

columns = ['sold_price', 'sqft', 'beds', 'baths', 'latitude', 'longitude']
df = df[columns].dropna().copy()  # Use .copy() to avoid SettingWithCopyWarning

# Normalize data
features = ['sqft', 'beds', 'baths']
scaler = MinMaxScaler()
X = scaler.fit_transform(df[features])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            sqft_min = int(request.form["sqft_min"])
            sqft_max = int(request.form["sqft_max"])
            beds = int(request.form["beds"])
            baths = int(request.form["baths"])
        except (ValueError, KeyError):
            flash("Please enter valid numbers for square footage range, bedrooms, and bathrooms.")
            return render_template("index.html", map_generated=False)

        filtered_homes = df[
            (df["sqft"] >= sqft_min) & 
            (df["sqft"] <= sqft_max) & 
            (df["beds"] == beds) & 
            (df["baths"] == baths)
        ]
        user_input = {
            "beds": beds,
            "baths": baths
        }

        # Compute similarity scores
        #user_vector = scaler.transform([[user_input[f] for f in features]])
        #df["similarity"] = cosine_similarity(user_vector, X)[0]

        # Create Folium Map
        m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=10)
        cluster = MarkerCluster().add_to(m)

        # Add markers
        for _, row in filtered_homes.iterrows():
            popup = f"""
            <div style="font-family: Arial; font-size: 14px; color: black;">
                <b>Price:</b> <span style="color: green;">${row['sold_price']:,.0f}</span><br>
                <b>Sqft:</b> {row['sqft']}<br>
                <b>Beds:</b> {row['beds']}<br>
                <b>Baths:</b> {row['baths']}<br>
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