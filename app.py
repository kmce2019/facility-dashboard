from flask import Flask, jsonify
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

EXCEL_FILE = 'UporDown.xlsm'  # Your updated Excel filename

# Read the Excel file and return a clean DataFrame
def read_facility_data():
    df = pd.read_excel(EXCEL_FILE, header=0)  # explicitly set first row as header
    df.columns = df.columns.str.strip()  # clean column names
    
    # Optional: print columns to debug if needed
    print("Columns read:", df.columns.tolist())
    
    # Select only the columns you need
    df = df[['Facility', 'Latitude', 'Longitude', 'URL']].dropna()
    return df

# Check status of a single facility
def check_status(row):
    url = row['URL']
    try:
        response = requests.get(url, timeout=5)
        return {
            'facility': row['Facility'],
            'latitude': row['Latitude'],
            'longitude': row['Longitude'],
            'status': 'UP' if response.status_code == 200 else 'DOWN',
            'status_code': response.status_code
        }
    except Exception:
        return {
            'facility': row['Facility'],
            'latitude': row['Latitude'],
            'longitude': row['Longitude'],
            'status': 'DOWN',
            'status_code': 0
        }

@app.route('/status.json')
def status_json():
    df = read_facility_data()
    # For debugging: show columns and sample data in JSON response
    return jsonify({
        "columns": df.columns.tolist(),
        "sample_data": df.head(3).to_dict(orient="records")
    })

# Optional: route for a simple homepage
@app.route('/')
def index():
    return "Facility status API. Access data at /status.json"

if __name__ == '__main__':
    print("Available routes:", app.url_map)
    app.run(host='0.0.0.0', port=5000)
