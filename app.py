from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_excel('UpDown.xlsm')

    # Normalize column names
    df = df.rename(columns={
        'Facility Code': 'Facility',
        'lat': 'Latitude',
        'lon': 'Longitude'
    })

    # Drop rows with missing location or URL
    df = df.dropna(subset=['Latitude', 'Longitude', 'URL'])

    # Perform HTTP GET checks
    statuses = []
    for url in df['URL']:
        try:
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            status = 'Up' if status_code == 200 else 'Down'
        except:
            status_code = None
            status = 'Down'
        statuses.append((status, status_code))

    df['Status'], df['StatusCode'] = zip(*statuses)

    data = df.to_dict(orient='records')
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
