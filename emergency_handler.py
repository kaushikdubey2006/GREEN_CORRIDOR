# emergency_handler.py
from db import get_connection

def handle_emergency(road_id, emergency_type):
    """
    Triggers an emergency on a specific road.
    - Logs the emergency
    - Forces all signals to RED
    - Gives immediate GREEN to the emergency road (Green Corridor start)
    """

    conn = get_connection()
    if conn is None:
        print("❌ DB connection failed in handle_emergency")
        return

    cur = conn.cursor()

    try:
        # 1. Log emergency
        cur.execute("""
            INSERT INTO emergency_logs (road_id, emergency_type, status)
            VALUES (%s, %s, 'ACTIVE')
        """, (road_id, emergency_type))

        # 2. Set all signals RED
        cur.execute("""
            UPDATE signal_status
            SET signal_color='RED', green_time=0
        """)

        # 3. Give GREEN to emergency road
        cur.execute("""
            REPLACE INTO signal_status (road_id, signal_color, green_time)
            VALUES (%s, 'GREEN', 40)
        """, (road_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("❌ Error in handle_emergency:", e)

    finally:
        cur.close()
        conn.close()


def clear_emergency(road_id=None):
    """
    Clears emergency state.
    - If road_id given → clears that specific road emergency
    - If not given → clears all active emergencies
    """

    conn = get_connection()
    if conn is None:
        print("❌ DB connection failed in clear_emergency")
        return

    cur = conn.cursor()

    try:
        if road_id:
            cur.execute("""
                UPDATE emergency_logs
                SET status='CLEARED'
                WHERE road_id=%s AND status='ACTIVE'
            """, (road_id,))
        else:
            cur.execute("""
                UPDATE emergency_logs
                SET status='CLEARED'
                WHERE status='ACTIVE'
            """)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("❌ Error in clear_emergency:", e)

    finally:
        cur.close()
        conn.close()
