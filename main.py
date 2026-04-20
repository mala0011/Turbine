from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

latest_sensor_data = {}


class SensorData(BaseModel):
    turbine_id: str
    temperature: float
    vibration: float
    rpm: int


def calculate_status(data: dict) -> dict:
    temperature = data["temperature"]
    vibration = data["vibration"]

    if temperature > 80 or vibration > 8:
        status = "critical"
        message = "Høj risiko for fejl"
    elif temperature > 65 or vibration > 5:
        status = "warning"
        message = "Turbinen bør overvåges"
    else:
        status = "ok"
        message = "Turbinen kører normalt"

    return {
        "turbine_id": data["turbine_id"],
        "sensor_data": data,
        "status": status,
        "message": message
    }


@app.get("/")
def root():
    return {"message": "Turbine API virker"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):
    latest_sensor_data[data.turbine_id] = data.model_dump()
    return {
        "message": "Sensordata modtaget",
        "data": latest_sensor_data[data.turbine_id]
    }


@app.get("/turbine-status/{turbine_id}")
def get_turbine_status(turbine_id: str):
    data = latest_sensor_data.get(turbine_id)

    if not data:
        return {
            "turbine_id": turbine_id,
            "status": "unknown",
            "message": "Ingen data modtaget endnu"
        }

    return calculate_status(data)


@app.get("/turbines")
def get_all_turbines():
    turbines = []
    for data in latest_sensor_data.values():
        turbines.append(calculate_status(data))
    return {"turbines": turbines}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="da">
    <head>
        <meta charset="UTF-8">
        <title>Turbine Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 30px;
                background: #f4f6f8;
            }
            h1 {
                margin-bottom: 20px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 20px;
            }
            .card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .ok {
                border-left: 8px solid green;
            }
            .warning {
                border-left: 8px solid orange;
            }
            .critical {
                border-left: 8px solid red;
            }
            .unknown {
                border-left: 8px solid gray;
            }
            .small {
                color: #555;
                margin-top: 8px;
            }
        </style>
    </head>
    <body>
        <h1>Turbine Dashboard</h1>
        <p>Opdateres automatisk hvert 5. sekund</p>
        <div id="dashboard" class="grid"></div>

        <script>
            async function loadTurbines() {
                const response = await fetch('/turbines');
                const data = await response.json();
                const dashboard = document.getElementById('dashboard');
                dashboard.innerHTML = '';

                if (!data.turbines || data.turbines.length === 0) {
                    dashboard.innerHTML = '<p>Ingen turbinedata endnu.</p>';
                    return;
                }

                data.turbines.forEach(turbine => {
                    const card = document.createElement('div');
                    card.className = 'card ' + turbine.status;

                    card.innerHTML = `
                        <h2>${turbine.turbine_id}</h2>
                        <p><strong>Status:</strong> ${turbine.status}</p>
                        <p><strong>Besked:</strong> ${turbine.message}</p>
                        <p><strong>Temperatur:</strong> ${turbine.sensor_data.temperature} °C</p>
                        <p><strong>Vibration:</strong> ${turbine.sensor_data.vibration}</p>
                        <p><strong>RPM:</strong> ${turbine.sensor_data.rpm}</p>
                    `;

                    dashboard.appendChild(card);
                });
            }

            loadTurbines();
            setInterval(loadTurbines, 5000);
        </script>
    </body>
    </html>
    """
