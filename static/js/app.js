    let timeout = null;

    function updateAndPredict() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const formData = {
                beds: document.getElementById("bedrooms").value,
                baths: document.getElementById("full_baths").value,
                sqft: document.getElementById("sqft").value,
                lot_sqft: document.getElementById("lot_size").value
            };
            console.log("Submitting Data:", formData);
        //     document.getElementById("predictedPrice").innerText = "Calculating...";
            document.getElementById("predictedPrice").innerText = ("See Console");
        //     fetch("http://localhost:5000/predict", {
        //         method: "POST",
        //         headers: { "Content-Type": "application/json" },
        //         body: JSON.stringify(formData)
        //     })
        //     .then(response => response.json())
        //     .then(data => {
        //         document.getElementById("predictedPrice").innerText = "$" + data.predicted_price.toLocaleString();
        //     })
        //     .catch(error => {
        //         console.error("Error:", error);
        //         document.getElementById("predictedPrice").innerText = "Error fetching price";
        //     });

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
        document.getElementById("predictedPrice").innerText = "Awaiting input...";
    }
