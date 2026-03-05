/* ================= GLOBAL STATE ================= */
let roadsData = [];

/* ================= ON LOAD ================= */
document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM Loaded");

    initLeafletMap();
    loadCities();

    // Bind activate button safely
    const btn = document.querySelector("button[onclick='activateRoute()']");
    if (!btn) {
        console.warn("⚠ Activate Route button not found");
    }
});

/* ================= LOAD CITIES ================= */
function loadCities() {
    fetch("/cities")
        .then(res => res.json())
        .then(cities => {
            console.log("✅ Cities received:", cities);

            const citySel = document.getElementById("citySelect");
            const src = document.getElementById("sourceSelect");
            const dst = document.getElementById("destinationSelect");

            if (!citySel || !src || !dst) {
                console.error("❌ Dropdown elements missing in HTML");
                return;
            }

            // reset all
            citySel.innerHTML = `<option value="">Select City</option>`;
            src.innerHTML = `<option value="">Select Source</option>`;
            dst.innerHTML = `<option value="">Select Destination</option>`;

            cities.forEach(city => {
                citySel.innerHTML += `<option value="${city}">${city}</option>`;
            });

            // bind once
            citySel.onchange = onCityChange;
        })
        .catch(err => console.error("❌ City fetch error:", err));
}

/* ================= CITY CHANGE ================= */
function onCityChange() {
    const city = document.getElementById("citySelect").value;
    const src = document.getElementById("sourceSelect");
    const dst = document.getElementById("destinationSelect");

    src.innerHTML = `<option value="">Select Source</option>`;
    dst.innerHTML = `<option value="">Select Destination</option>`;

    if (!city) {
        console.log("ℹ City not selected");
        return;
    }

    console.log("📍 Selected city:", city);

    fetch(`/roads?city=${encodeURIComponent(city)}`)
        .then(res => res.json())
        .then(roads => {
            console.log("🛣 Roads received:", roads);

            if (!Array.isArray(roads) || roads.length === 0) {
                console.warn("⚠ No roads found for city:", city);
                return;
            }

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
        if (!r.road_id || !r.road_name) return;

        const opt = `<option value="${r.road_id}">${r.road_name}</option>`;
        src.innerHTML += opt;
        dst.innerHTML += opt;
    });

    console.log("✅ Source & Destination populated");
}

/* ================= ACTIVATE ROUTE ================= */
function activateRoute() {
    const source = document.getElementById("sourceSelect").value;
    const destination = document.getElementById("destinationSelect").value;

    if (!source || !destination) {
        alert("Please select source and destination");
        return;
    }

    console.log("🚑 Activating route:", source, destination);

    fetch("/route/activate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, destination })
    })
        .then(res => res.json())
        .then(data => {
            console.log("🚦 Route response:", data);

            if (!data.route || data.route.length === 0) {
                alert("No route found");
                return;
            }

            drawLeafletRoute(data.route);
            showRouteDetails(data.route);
        })
        .catch(err => console.error("❌ Route activate error:", err));
}

/* ================= ROUTE DETAILS ================= */
function showRouteDetails(route) {
    const box = document.getElementById("routeDetails");
    if (!box) return;

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
    if (!box) return;

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
