from flask import Flask, jsonify
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

EXCEL_FILE = '/app/UporDown.xlsm'

def read_facility_data():
    df = pd.read_excel(EXCEL_FILE, header=0)  # explicitly set first row as header
    df.columns = df.columns.str.strip()  # clean column names
    df = df[['Facility', 'Latitude', 'Longitude', 'URL']].dropna()
    return df

def check_status(row):
    url = row['URL']
    try:
        response = requests.get(url, timeout=5)
        status = 'UP' if response.status_code == 200 else 'DOWN'
        status_code = response.status_code
    except Exception:
        status = 'DOWN'
        status_code = 0

    return {
        'facility': row['Facility'],
        'latitude': row['Latitude'],
        'longitude': row['Longitude'],
        'status': status,
        'status_code': status_code
    }

@app.route('/status.json')
def status_json():
    df = read_facility_data()
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_status, [row for _, row in df.iterrows()]))

    return jsonify({"data": results})

@app.route('/')
def index():
    return "Facility status API. Access data at /status.json"

if __name__ == '__main__':
    print("Available routes:", app.url_map)
    app.run(host='0.0.0.0', port=5000)
