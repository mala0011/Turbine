import random
import time
import requests

API_URL = "http://127.0.0.1:8000/sensor-data"

turbines = {
    "T-101": {"temperature": 72.0, "vibration": 6.0, "rpm": 1450},
    "T-102": {"temperature": 55.0, "vibration": 3.0, "rpm": 1380},
    "T-103": {"temperature": 85.0, "vibration": 9.0, "rpm": 1600},
}


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


while True:
    for turbine_id, values in turbines.items():
        values["temperature"] = clamp(
            values["temperature"] + random.uniform(-1.5, 1.5), 40, 95
        )
        values["vibration"] = clamp(
            values["vibration"] + random.uniform(-0.4, 0.4), 1, 10
        )
        values["rpm"] = int(clamp(
            values["rpm"] + random.randint(-25, 25), 1200, 1700
        ))

        payload = {
            "turbine_id": turbine_id,
            "temperature": round(values["temperature"], 1),
            "vibration": round(values["vibration"], 1),
            "rpm": values["rpm"],
        }

        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            print(f"Sendte {turbine_id}: {payload} -> {response.status_code}")
        except Exception as e:
            print(f"Fejl ved sending af {turbine_id}: {e}")

    print("Venter 5 sekunder...\n")
    time.sleep(5)
    