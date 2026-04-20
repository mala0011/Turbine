# Turbine-API

Et simpelt projekt til overvågning af vindturbiner.

## Indhold

* FastAPI backend
* simulator til sensordata
* dashboard på `/dashboard`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start projektet

Terminal 1:

```bash
uvicorn api.main:app --reload
```

Terminal 2:

```bash
python simulator.py
```

## Åbn dashboard

```text
http://127.0.0.1:8000/dashboard
```

## API endpoints

* `/`
* `/health`
* `/sensor-data`
* `/turbine-status/{turbine_id}`
* `/turbines`
* `/dashboard`
