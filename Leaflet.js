/* =================================================
   LEAFLET MAP MODULE (FINAL & CLEAN)
   - Single map instance
   - Markers (signals)
   - Route polyline (green corridor)
================================================= */

let map = null;
let markers = [];
let routeLine = null;

/* ================= INIT MAP ================= */
function initLeafletMap() {
    // 🔴 IMPORTANT: prevent double init
    if (map !== null) return;

    map = L.map("map").setView([28.6139, 77.2090], 12);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors"
    }).addTo(map);
}

/* ================= UPDATE SIGNAL MARKERS ================= */
function updateLeafletSignals(roads) {
    if (!map) return;

    // remove old markers
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    roads.forEach(r => {
        if (!r.latitude || !r.longitude) return;

        const color = r.signal_color === "GREEN" ? "green" : "red";

        const marker = L.circleMarker(
            [r.latitude, r.longitude],
            {
                radius: 8,
                color: color,
                fillColor: color,
                fillOpacity: 0.9
            }
        ).addTo(map);

        marker.bindPopup(`
            <b>${r.road_name}</b><br/>
            Signal: ${r.signal_color}<br/>
            Green Time: ${r.green_time}s
        `);

        markers.push(marker);
    });
}

/* ================= DRAW ROUTE ================= */
function drawLeafletRoute(routeRoads) {
    if (!map || !routeRoads || routeRoads.length === 0) return;

    // remove old route
    if (routeLine) {
        map.removeLayer(routeLine);
        routeLine = null;
    }

    const latlngs = routeRoads.map(r => [r.latitude, r.longitude]);

    routeLine = L.polyline(latlngs, {
        color: "lime",
        weight: 6,
        opacity: 0.9
    }).addTo(map);

    map.fitBounds(routeLine.getBounds());
}

/* ================= CLEAR ROUTE ================= */
function clearLeafletRoute() {
    if (routeLine && map) {
        map.removeLayer(routeLine);
        routeLine = null;
    }
}
