// Initialize map
const map = L.map('map').setView([44.95, -93.09], 11); // Minneapolis default
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Elements
const beds = document.getElementById('beds');
const baths = document.getElementById('baths');
const sqft = document.getElementById('sqft');
const lot = document.getElementById('lot');

const bedsVal = document.getElementById('bedsVal');
const bathsVal = document.getElementById('bathsVal');
const sqftVal = document.getElementById('sqftVal');
const lotVal = document.getElementById('lotVal');
const predictedPrice = document.getElementById('predictedPrice');

// Dummy model function (replace with backend call later)
function predictPrice(beds, baths, sqft, lot) {
  return Math.round((beds * 50000) + (baths * 40000) + (sqft * 150) + (lot * 2));
}

// Update everything on slider change
function update() {
  bedsVal.textContent = beds.value;
  bathsVal.textContent = baths.value;
  sqftVal.textContent = sqft.value;
  lotVal.textContent = lot.value;

  const price = predictPrice(+beds.value, +baths.value, +sqft.value, +lot.value);
  predictedPrice.textContent = price.toLocaleString();

  updateMap(price);
}

// Example map update
function updateMap(price) {
  // You can filter GeoJSON or change marker colors based on similarity
  // For now, just display a popup
  L.popup()
    .setLatLng([44.9778, -93.2650])
    .setContent(`Predicted Price: $${price.toLocaleString()}`)
    .openOn(map);
}

// Attach listeners
[beds, baths, sqft, lot].forEach(input => input.addEventListener('input', update));

// Initial update
update();