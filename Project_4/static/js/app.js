// Initialize map
const map = L.map('map').setView([44.9778, -93.2650], 11); 
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Elements
const beds = document.getElementById('beds');
const baths = document.getElementById('baths');
const sqft = document.getElementById('sqft');
const lot = document.getElementById('lot_sqft');

const bedsVal = document.getElementById('bedsVal');
const bathsVal = document.getElementById('bathsVal');
const sqftVal = document.getElementById('sqftVal');
const lotVal = document.getElementById('lotVal');

const predictedPrice = document.getElementById('predictedPrice');

let markers = [];

// Add similar homes to map
function updateMapWithSimilarHomes(homes) {
  // Clear old markers
  markers.forEach(m => map.removeLayer(m));
  markers = [];

homes.forEach(home => {
  home.latitude = Number(home.latitude);
  home.longitude = Number(home.longitude);

  if (!isNaN(home.latitude) && !isNaN(home.longitude)) {
    // Build address string if street, city, and zip exist
    let address = "";
    if (home.street && home.city && home.zip) {
      address = `${home.street}, ${home.city}, ${home.zip}`;
    }

    const marker = L.circleMarker([home.latitude, home.longitude], {
      radius: 8,
      color: "#007BFF",
      fillOpacity: 0.6
    }).bindPopup(`
      <b>Price:</b> $${home.sold_price.toLocaleString()}<br>
      <b>Beds:</b> ${home.beds}<br>
      <b>Baths:</b> ${home.baths}<br>
      <b>Sqft:</b> ${home.sqft}<br>
      <b>Lot Sqft:</b> ${home.lot_sqft}<br>
      ${address ? `<b>Address:</b> ${address}<br>` : ""}
    `);

    marker.addTo(map);
    markers.push(marker);
  } else {
    console.warn("Skipping home with invalid latitude/longitude:", home);
  }
});
}

// Predict function
function update() {
  const inputData = {
    beds: +beds.value,
    baths: +baths.value,
    sqft: +sqft.value,
    lot: +lot.value
  };

  bedsVal.textContent = inputData.beds;
  bathsVal.textContent = inputData.baths;
  sqftVal.textContent = inputData.sqft;
  lotVal.textContent = inputData.lot;

  console.log("Sending input:", inputData);

  // Update Price
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(inputData)
  })
    .then(res => res.json())
    .then(data => {
      const price = data.predicted_price;
      predictedPrice.textContent = `$${price.toLocaleString()}`;
    });

  // Update map
  fetch("/similar-homes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(inputData)
  })
    .then(res => res.json())
    .then(homes => {
      updateMapWithSimilarHomes(homes);
    });
}

// Attach listeners
[beds, baths, sqft, lot].forEach(input =>
  input.addEventListener('input', update)
);

// Debounce wrapper
function debounce(func, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), delay);
  };
}

// Replace update() with debounced version
const debouncedUpdate = debounce(update, 300);

// Use debounced version in listeners
[beds, baths, sqft, lot].forEach(input =>
  input.addEventListener('input', debouncedUpdate)
);

// Initial update
update();
