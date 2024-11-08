mapboxgl.accessToken = 'pk.eyJ1Ijoia29seWE3IiwiYSI6ImNsczBhdzM4dTAwYWgyaW14eHgxbm1saDMifQ.U7Q43WKnBARLAOqlJzEwTg';
var map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/mapbox/streets-v12', // stylesheet location
        zoom: 0,
        attributionControl: false
});
map.on('load', function() {
    map.on('click', function(e) {
        selectedLocation = {
            lat: e.lngLat.lat,
            lon: e.lngLat.lng
        };
        console.log("Selected location:", selectedLocation);
        if (tappedMarker) {
            tappedMarker.remove();
        }
        tappedMarker = new mapboxgl.Marker().setLngLat(e.lngLat).addTo(map).setPopup(new mapboxgl.Popup().setHTML("You tapped this location")).togglePopup();
    });

});

// Code to call the python API
console.log("Going to call api");
fetch('http://localhost:5001/api/ping')
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
        style = 'mapbox://styles/mapbox/satellite-streets-v11';
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

