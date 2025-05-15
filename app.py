from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_excel('UpDown.xlsm')

    # Ensure required columns exist
    required_cols = {'Facility', 'Latitude', 'Longitude', 'URL'}
    if not required_cols.issubset(df.columns):
        return "Missing required columns in the Excel file.", 500

    results = []
    for _, row in df.iterrows():
        url = row['URL']
        try:
            resp = requests.get(url, timeout=5)
            status_code = resp.status_code
            status = 'Up' if status_code == 200 else 'Down'
        except Exception:
            status_code = 0
            status = 'Down'

        results.append({
            'Facility': row['Facility'],
            'Latitude': row['Latitude'],
            'Longitude': row['Longitude'],
            'URL': url,
            'Status': status,
            'StatusCode': status_code
        })

    return render_template('dashboard.html', data=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
