# traffic_controller.py
from db import get_connection

# --------------------------------------------------
# Green Time Calculation Logic
# --------------------------------------------------
def calculate_green_time(vehicle_count):
    """
    Decide green signal duration based on vehicle density.
    Rule-based (interview-safe).
    """
    if vehicle_count <= 5:
        return 10
    elif vehicle_count <= 15:
        return 20
    else:
        return 30


# --------------------------------------------------
# Core Traffic Signal Logic
# --------------------------------------------------
def update_signal_logic():
    """
    Core traffic optimization logic.

    Flow:
    1. Fetch all roads with latest vehicle counts
    2. Sort roads based on congestion
    3. Set all signals RED
    4. Give GREEN to the most congested road
    5. Prepare frontend-ready data (map + dashboard)
    """

    conn = get_connection()
    if conn is None:
        print("❌ DB connection failed in traffic_controller")
        return []

    cur = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Fetch roads + traffic data
        cur.execute("""
            SELECT 
                r.road_id,
                r.road_name,
                IFNULL(t.vehicle_count, 0) AS vehicle_count
            FROM roads r
            LEFT JOIN traffic_data t ON r.road_id = t.road_id
        """)
        roads = cur.fetchall()

        if not roads:
            return []

        # 2️⃣ Sort roads by congestion
        roads_sorted = sorted(
            roads, key=lambda x: x['vehicle_count'], reverse=True
        )

        # 3️⃣ Set all signals RED
        cur.execute("""
            UPDATE signal_status
            SET signal_color='RED', green_time=0
        """)

        # 4️⃣ Assign GREEN to highest traffic road
        top_road = roads_sorted[0]
        green_time = calculate_green_time(top_road['vehicle_count'])

        cur.execute("""
            REPLACE INTO signal_status (road_id, signal_color, green_time)
            VALUES (%s, 'GREEN', %s)
        """, (top_road['road_id'], green_time))

        conn.commit()

        # 5️⃣ Prepare frontend-ready response (Map + UI)
        for road in roads_sorted:
            # Dummy coordinates (OK for demo & photo)
            road['latitude'] = 28.60 + (road['road_id'] * 0.01)
            road['longitude'] = 77.10 + (road['road_id'] * 0.01)

            if road['road_id'] == top_road['road_id']:
                road['signal_color'] = 'GREEN'
                road['green_time'] = green_time
            else:
                road['signal_color'] = 'RED'
                road['green_time'] = 0

        return roads_sorted

    except Exception as e:
        conn.rollback()
        print("❌ Error in traffic_controller:", e)
        return []

    finally:
        cur.close()
        conn.close()
