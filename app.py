from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)

def get_status(url):
    try:
        response = requests.get(url, timeout=5)
        return 200 if response.status_code == 200 else response.status_code
    except Exception:
        return 0  # Unreachable or bad request

@app.route('/')
def index():
    df = pd.read_excel('UpDown.xlsm')

    # Ensure all necessary columns exist
    required_columns = {'Facility', 'Latitude', 'Longitude', 'URL'}
    if not required_columns.issubset(df.columns):
        return "Missing one or more required columns in Excel file."

    # Drop any rows without lat/lon or URL
    df = df.dropna(subset=['Latitude', 'Longitude', 'URL'])

    data = []
    for _, row in df.iterrows():
        try:
            lat = float(row['Latitude'])
            lon = float(row['Longitude'])
            url = row['URL']
            status = get_status(url)
            data.append({
                'Facility': row['Facility'],
                'Latitude': lat,
                'Longitude': lon,
                'URL': url,
                'Status': 'UP' if status == 200 else f'DOWN ({status})',
                'StatusCode': status
            })
        except:
            continue  # Skip bad rows

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
