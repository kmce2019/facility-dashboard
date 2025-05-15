from flask import Flask, jsonify
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

EXCEL_FILE = 'UporDown.xlsm'

# Read the Excel file and return a clean DataFrame
def read_facility_data():
    df = pd.read_excel(EXCEL_FILE)
    # Strip whitespace from column headers to avoid hidden spaces causing errors
    df.columns = df.columns.str.strip()
    print("Columns in Excel:", df.columns.tolist())  # Debug print for columns
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_status, [row for _, row in df.iterrows()]))
    return jsonify(results)

@app.route('/')
def index():
    return "Facility status API. Access data at /status.json"

if __name__ == '__main__':
    print("Available routes:", app.url_map)
    app.run(host='0.0.0.0', port=5000)
