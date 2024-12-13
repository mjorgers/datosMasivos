mapboxgl.accessToken = 'pk.eyJ1Ijoia29seWE3IiwiYSI6ImNsczBhdzM4dTAwYWgyaW14eHgxbm1saDMifQ.U7Q43WKnBARLAOqlJzEwTg';
var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/satellite-streets-v12',
        zoom: 0,
        attributionControl: false
});

// Add at the beginning of the file
let stockUpdateInterval;

function updateStockPrices() {
    const url = `http://localhost:5001/api/stock_price?stock_symbols=MKHO-MY,UVPOF,SOPS-MY,GOOG,AAPL,NVDA`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('stocks-container');
            container.innerHTML = ''; // Clear existing content
            
            data.stock_prices.forEach(stockData => {
                const stockCard = document.createElement('div');
                stockCard.className = 'stock-card';
                
                // Parse the timestamp
                const timestamp = new Date(stockData.timestamp);
                const formattedTime = timestamp.toLocaleTimeString();
                
                stockCard.innerHTML = `
                    <div class="stock-symbol">${stockData.symbol}</div>
                    <div class="stock-price">$${parseFloat(stockData.price).toFixed(2)}</div>
                    <div class="stock-timestamp">Last updated: ${formattedTime}</div>
                `;
                container.appendChild(stockCard);
            });
        })
        .catch(error => {
            console.error('Error fetching stock data:', error);
            createAlert({
                type: "error",
                message: "Failed to fetch stock data",
                time: 3000
            });
        });
}

map.on('load', function() {
  fetch('demo.json')
  .then(response => response.json())
  .then(data => {
      addOilMillMarkers(data);
      updatePolicyData(data);
  })
  .catch(error => console.error('Error loading data:', error));
    
    // Initial stock data load
    updateStockPrices();
    
    // Set up interval for updates
    stockUpdateInterval = setInterval(updateStockPrices, 5000);

    createAlert({'type': 'success', 'message': 'Map loaded successfully', 'time': 3000});
});

// Update the updatePolicyData function to add click handlers
function updatePolicyData(data) {
    const container = document.getElementById('policies-container');
    container.innerHTML = '';
    
    data.forEach(country => {
        const policyCard = document.createElement('div');
        policyCard.className = 'policy-card';
        
        country.indicators.forEach(indicator => {
            policyCard.innerHTML = `
                <div class="policy-title">${country.country_name} - ${indicator.name}</div>
                <div class="policy-value">Score: ${indicator.value}</div>
                <div class="policy-date">Last updated: ${indicator.last_update}</div>
            `;
        });
        
        // Add click handler
        policyCard.style.cursor = 'pointer';
        policyCard.addEventListener('click', () => {
            flyToCountry(country.country_name);
        });
        
        container.appendChild(policyCard);
    });
}
// Add cleanup when needed (e.g., when switching pages)
function cleanup() {
    if (stockUpdateInterval) {
        clearInterval(stockUpdateInterval);
    }
}

function addOilMillMarkers(data) {
    // Remove existing markers if needed
    if (window.oilMillMarkers) {
        window.oilMillMarkers.forEach(marker => marker.remove());
    }
    window.oilMillMarkers = [];

    data.forEach(country => {
        country.oil_mills.forEach(mill => {
            const coordinates = [mill.coordinates.longitude, mill.coordinates.latitude];
            
            // Create popup content with mill details
            const popupContent = `
                <h3>${mill.mill}</h3>
                <p>Parent Company: ${mill.parent_company}</p>
                <p>Group: ${mill.group}</p>
                <p>RSPO Type: ${mill.RSPO_type !== 'nan' ? mill.RSPO_type : 'Not certified'}</p>
                <p>Confidence Level: ${mill.confidence_level}</p>
                <p>Location: ${mill.providence}, ${mill.district}</p>
            `;

            // Create marker and popup
            const marker = new mapboxgl.Marker()
                .setLngLat(coordinates)
                .setPopup(new mapboxgl.Popup().setHTML(popupContent))
                .addTo(map);

            window.oilMillMarkers.push(marker);
        });
    });

    // Fit map to show all markers
    if (window.oilMillMarkers.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        window.oilMillMarkers.forEach(marker => {
            bounds.extend(marker.getLngLat());
        });
        map.fitBounds(bounds, { padding: 50 });
    }
}

// Code to call the python API
console.log("Going to call api");

const stockSymbols = 'MKHO-MY,UVPOF,SOPS-MY';

// Construct the URL with query parameters
const url = `http://localhost:5001/api/stock_price?stock_symbols=${encodeURIComponent(stockSymbols)}`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log("API Response:", data);
    })
    .catch(error => {
        console.error('Error fetching API:', error);
    });


var tappedMarker = null;
var selectedLocation = null;
console.log("Selected location:", selectedLocation);
map.addLayer({
        id: 'tileLayer',
        type: 'raster',
        source: {
                type: 'raster',
                tiles: ['https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=ZTKYDYAecEkhrCpOleVE'],
                tileSize: 256,
                attribution: '© <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        },
        minzoom: 0,
        maxzoom: 19
});


function switchMapTheme(theme) {
    if (theme === 'dark') {
        style = 'mapbox://styles/mapbox/dark-v11';
    } else if (theme === 'light') {
        style = 'mapbox://styles/mapbox/streets-v11';
    } else if (theme === 'satellite') {
        style = 'mapbox://styles/mapbox/satellite-streets-v12';
    } else if (theme === 'globe' ) {
        style = 'mapbox://styles/mapbox/streets-v12';
    }
    map.setStyle(style);
}

function searchLocation() {
    var location = document.getElementById("searchInput").value;
    if (location) {
      var url = "https://nominatim.openstreetmap.org/search?format=json&q=" + encodeURIComponent(location);
      fetch(url).then(response => response.json()).then(data => {
        if (data.length > 0) {
          var results = data.map(result => ({
            display_name: result.display_name,
            lat: parseFloat(result.lat),
            lon: parseFloat(result.lon)
          }));
          var resultsList = document.getElementById("resultsList");
          // Clear the results list before appending new results
          while (resultsList.firstChild) {
            resultsList.removeChild(resultsList.firstChild);
          }
          results.forEach((result, index) => {
            var resultItem = document.createElement("div");
            resultItem.classList.add("result-item");
            resultItem.textContent = `${index + 1}. ${result.display_name}`;
            resultItem.addEventListener("click", function() {
              selectLocation(index, results);
            });
            resultsList.appendChild(resultItem);
          });
          openResultsModal();
          closeSearchModal();
        } else {
          alert("Location not found.");
        }
      }).catch(error => {
        console.error("Error:", error);
        alert("An error occurred while searching for the location.");
      });
    }
}

function selectLocation(index, results) {
    if (index >= 0 && index < results.length) {
      selectedLocation = results[index];
      console.log("Selected location:", selectedLocation);
      var lngLat = [selectedLocation.lon, selectedLocation.lat];
      if (tappedMarker) {
        tappedMarker.remove();
      }
      tappedMarker = new mapboxgl.Marker().setLngLat(lngLat).addTo(map).setPopup(new mapboxgl.Popup().setHTML("You selected: " + selectedLocation.display_name)).togglePopup();
      map.flyTo({center: lngLat,
        zoom: 16 });
    } else {
      alert("Invalid selection.");
    }
    closeModal();
}
function openResultsModal() {
    var modal = document.getElementById("resultsModal");
    modal.style.display = "block";
}

function openSettings() {
    var modal = document.getElementById("settingsModal");
    modal.style.display = "block";
}

function openSearchModal() {
    var modal = document.getElementById("searchModal");
    modal.style.display = "block";
}

function closeSearchModal() {
    var modal = document.getElementById("searchModal");
    modal.style.display = "none";
}

function closeModal() {
    var modal = document.getElementById("resultsModal");
    modal.style.display = "none";
    var settingsModal = document.getElementById("settingsModal");
    settingsModal.style.display = "none";
}

// Add this new function to get country coordinates and fly to them
function flyToCountry(countryName) {
    // Create Geocoding API URL
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(countryName)}.json?access_token=${mapboxgl.accessToken}&types=country`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.features && data.features.length > 0) {
                const bounds = data.features[0].bbox;
                map.fitBounds([
                    [bounds[0], bounds[1]], // southwestern corner
                    [bounds[2], bounds[3]]  // northeastern corner
                ], {
                    padding: 50,
                    duration: 2000
                });
            } else {
                createAlert({
                    type: "error",
                    message: `Could not find coordinates for ${countryName}`,
                    time: 3000
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            createAlert({
                type: "error",
                message: "Failed to fly to country",
                time: 3000
            });
        });
}

