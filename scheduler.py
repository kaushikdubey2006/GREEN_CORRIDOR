# scheduler.py

import threading
import time

# ==================================================
# Global Thread Lock (Critical Section Protection)
# ==================================================
lock = threading.Lock()

# ==================================================
# Utility Functions
# ==================================================

def wait(seconds):
    """
    Pause execution for given seconds.
    Used to simulate real-time traffic signal delays.
    """
    time.sleep(seconds)


def critical_section(func, *args, **kwargs):
    """
    Executes a function inside a critical section
    using a mutex lock to prevent race conditions.

    Example:
        critical_section(update_signal_logic)

    Ensures:
    - Only one thread updates traffic signals at a time
    - Emergency and traffic logic never collide
    """
    with lock:
        return func(*args, **kwargs)


# ==================================================
# Periodic Scheduler (Auto Traffic Optimization)
# ==================================================

def run_periodically(func, interval_seconds, *args, **kwargs):
    """
    Runs a function repeatedly at fixed intervals
    inside a daemon thread.

    Parameters:
    - func: function to run
    - interval_seconds: time gap between runs
    - *args, **kwargs: arguments for the function

    Example:
        run_periodically(update_signal_logic, 30)
    """

    def wrapper():
        while True:
            try:
                critical_section(func, *args, **kwargs)
            except Exception as e:
                print("❌ Scheduler Error:", e)

            time.sleep(interval_seconds)

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    return thread
