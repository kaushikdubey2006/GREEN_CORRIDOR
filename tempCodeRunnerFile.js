/* ================= GLOBAL STATE ================= */
let roadsData = [];

/* ================= ON LOAD ================= */
document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM Loaded");

    initLeafletMap();
    loadCities();
});

/* ================= LOAD CITIES ================= */
function loadCities() {
    fetch("/cities")
        .then(res => res.json())
        .then(cities => {
            console.log("✅ Cities:", cities);

            const citySel = document.getElementById("citySelect");
            if (!citySel) {
                console.error("❌ citySelect not found");
                return;
            }

            citySel.innerHTML = `<option value="">Select City</option>`;

            cities.forEach(city => {
                citySel.innerHTML += `
                    <option value="${city}">${city}</option>
                `;
            });

            citySel.addEventListener("change", onCityChange);
        })
        .catch(err => console.error("❌ City fetch error:", err));
}

/* ================= CITY CHANGE ================= */
function onCityChange(e) {
    const city = e.target.value;

    const src = document.getElementById("sourceSelect");
    const dst = document.getElementById("destinationSelect");

    if (!city) {
        src.innerHTML = `<option value="">Select Source</option>`;
        dst.innerHTML = `<option value="">Select Destination</option>`;
        return;
    }

    console.log("📍 Selected city:", city);

    fetch(`/roads?city=${encodeURIComponent(city)}`)
        .then(res => res.json())
        .then(roads => {
            console.log("🛣 Roads:", roads);

            roadsData = roads;

            fillDropdowns(roads);
            updateSignalPanel(roads);
            updateLeafletSignals(roads);
        })
        .catch(err => console.error("❌ Roads fetch error:", err));
}

/* ================= FILL SOURCE / DEST ================= */
function fillDropdowns(roads) {
    const src = document.getElementById("sourceSelect");
    const dst = document.getElementById("destinationSelect");

    src.innerHTML = `<option value="">Select Source</option>`;
    dst.innerHTML = `<option value="">Select Destination</option>`;

    roads.forEach(r => {
        src.innerHTML += `<option value="${r.road_id}">${r.road_name}</option>`;
        dst.innerHTML += `<option value="${r.road_id}">${r.road_name}</option>`;
    });

    console.log("✅ Source/Destination filled");
}

/* ================= ACTIVATE ROUTE ================= */
function activateRoute() {
    const source = document.getElementById("sourceSelect").value;
    const destination = document.getElementById("destinationSelect").value;

    if (!source || !destination) {
        alert("Please select source and destination");
        return;
    }

    fetch("/route/activate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, destination })
    })
    .then(res => res.json())
    .then(data => {
        console.log("🚑 Route activated:", data);

        if (data.route && data.route.length > 0) {
            drawLeafletRoute(data.route);
            showRouteDetails(data.route);
        }
    })
    .catch(err => console.error("❌ Route error:", err));
}

/* ================= ROUTE DETAILS ================= */
function showRouteDetails(route) {
    const box = document.getElementById("routeDetails");

    box.innerHTML = `
        Start: <b>${route[0].road_name}</b><br>
        End: <b>${route[route.length - 1].road_name}</b><br>
        Roads: <b>${route.length}</b><br>
        Mode: <b>Emergency Corridor</b>
    `;
}

/* ================= SIGNAL PANEL ================= */
function updateSignalPanel(roads) {
    const box = document.getElementById("signalList");
    box.innerHTML = "";

    roads.forEach(r => {
        box.innerHTML += `
            <div class="route-item">
                <b>${r.road_name}</b><br>
                Signal:
                <span class="${r.signal_color === 'GREEN' ? 'green' : 'red'}">
                    ${r.signal_color}
                </span>
            </div>
        `;
    });
}
