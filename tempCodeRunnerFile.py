from flask import Flask, request, jsonify, send_from_directory
from db import get_connection
from route_engine import calculate_optimal_route

app = Flask(__name__, static_url_path='', static_folder='../Frontend')

# ================= FRONTEND =================
@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/script.js")
def js():
    return send_from_directory("../Frontend", "script.js")

@app.route("/style.css")
def css():
    return send_from_directory("../Frontend", "style.css")

@app.route("/Leaflet.js")
def leaflet():
    return send_from_directory("../Frontend", "Leaflet.js")


# ================= API =================

# -------- GET CITIES --------
@app.route("/cities", methods=["GET"])
def get_cities():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT DISTINCT city_id, city_name
        FROM cities
        ORDER BY city_name
    """)
    data = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(data)


# -------- GET ROADS (BY CITY OPTIONAL) --------
@app.route("/roads", methods=["GET"])
def get_roads():
    city_id = request.args.get("city_id")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    if city_id:
        cur.execute("""
            SELECT r.road_id, r.road_name,
                   r.latitude, r.longitude,
                   IFNULL(s.signal_color,'RED') signal_color,
                   IFNULL(s.green_time,0) green_time
            FROM roads r
            LEFT JOIN signal_status s ON r.road_id = s.road_id
            WHERE r.city_id = %s
        """, (city_id,))
    else:
        cur.execute("""
            SELECT r.road_id, r.road_name,
                   r.latitude, r.longitude,
                   IFNULL(s.signal_color,'RED') signal_color,
                   IFNULL(s.green_time,0) green_time
            FROM roads r
            LEFT JOIN signal_status s ON r.road_id = s.road_id
        """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


# -------- ACTIVATE ROUTE --------
@app.route("/route/activate", methods=["POST"])
def activate_route():
    data = request.get_json()
    source = int(data["source"])
    destination = int(data["destination"])

    # Calculate route
    route_ids = calculate_optimal_route(source, destination)

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # Sab RED
    cur.execute("UPDATE signal_status SET signal_color='RED', green_time=0")

    # Route GREEN
    for rid in route_ids:
        cur.execute("""
            UPDATE signal_status
            SET signal_color='GREEN', green_time=40
            WHERE road_id=%s
        """, (rid,))

    # Route details for frontend
    placeholders = ",".join(["%s"] * len(route_ids))
    cur.execute(f"""
        SELECT road_id, road_name, latitude, longitude
        FROM roads
        WHERE road_id IN ({placeholders})
        ORDER BY FIELD(road_id, {placeholders})
    """, route_ids * 2)

    route_roads = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "status": "active",
        "route": route_roads
    })


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True, port=8000)
