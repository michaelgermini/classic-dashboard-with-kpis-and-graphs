# Banking Dashboard (Streamlit + Mini 3D)

Run a banking dashboard with KPIs, Plotly charts, and a mini 3D scene for data storytelling.

## Prerequisites
- Python 3.10+
- Windows PowerShell (or any shell)

## Quick setup
```powershell
python -m venv venv
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\python -m pip install -r requirements.txt
```

## Run the app
```powershell
.\venv\Scripts\python -m streamlit run app.py
```

## Structure
- `app.py`: entry point, KPIs, filters, charts, mini 3D
- `components/`: KPI cards, filters
- `viz/`: Plotly charts (2D) + mini 3D scene
- `services/`: data loading/generation
- `.streamlit/config.toml`: Streamlit theme

## Data
- If `data/sample/transactions.csv` does not exist, a synthetic dataset is generated and cached for future runs.

## Deploy
- Streamlit Community Cloud or Docker (to be added).
