# route_engine.py
from db import get_connection

def calculate_optimal_route(source_road_id, destination_road_id):
    """
    Simple & safe route logic (MVP):
    - Same city ke roads use karta hai
    - Source → Destination ke beech ke road_ids return karta hai
    - Future me Dijkstra / ML se replace ho sakta hai
    """

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # 1️⃣ Find city of source road
    cur.execute("""
        SELECT city_id FROM roads WHERE road_id=%s
    """, (source_road_id,))
    src = cur.fetchone()

    if not src:
        cur.close()
        conn.close()
        return []

    city_id = src["city_id"]

    # 2️⃣ Get all roads of that city (ordered by road_id)
    cur.execute("""
        SELECT road_id FROM roads
        WHERE city_id=%s
        ORDER BY road_id
    """, (city_id,))
    city_roads = [r["road_id"] for r in cur.fetchall()]

    cur.close()
    conn.close()

    # 3️⃣ Build route slice (source → destination)
    if source_road_id not in city_roads or destination_road_id not in city_roads:
        return []

    start_idx = city_roads.index(source_road_id)
    end_idx = city_roads.index(destination_road_id)

    if start_idx <= end_idx:
        route = city_roads[start_idx:end_idx + 1]
    else:
        route = city_roads[end_idx:start_idx + 1][::-1]

    return route
