    let timeout = null;

    function updateAndPredict() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const formData = {
                baths: document.getElementById("full_baths").value,
                beds: document.getElementById("bedrooms").value,
                lot_sqft: document.getElementById("lot_size").value,
                sqft: document.getElementById("sqft").value
                // beds_baths_ratio: document.getElementById("bedrooms").value/document.getElementById("full_baths").value,
                // lot_to_sqft_ratio: document.getElementById("lot_size").value/document.getElementById("sqft").value
            };
            console.log("Submitting Data:", formData);
       
            // d3.json("Model_Selection/sold_price_model.pkl").then((data) => {
            document.getElementById("predicted_price").innerText = "Calculating...";
            fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("predicted_Price").innerText = "$" + data.predicted_price.toLocaleString();
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementById("predicted_Price").innerText = "Error fetching price";
            });

            updateValues();
        }, 300);
    }

    function updateValues() {
        document.getElementById("bedroomsValue").innerText = document.getElementById("bedrooms").value;
        document.getElementById("fullBathsValue").innerText = document.getElementById("full_baths").value;
        document.getElementById("sqftValue").innerText = document.getElementById("sqft").value + " sq ft";
        document.getElementById("lotSizeValue").innerText = document.getElementById("lot_size").value + " sq ft";
    }

    function resetForm() {
        // Reset slider values
        document.getElementById("bedrooms").value = 0;
        document.getElementById("full_baths").value = 0;
        document.getElementById("sqft").value = 0;
        document.getElementById("lot_size").value = 0;

        // Update displayed values
        updateValues();

        // Clear predicted price
        document.getElementById("predicted_Price").innerText = "Awaiting input...";
    }
