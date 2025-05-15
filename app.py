from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load the spreadsheet
    df = pd.read_excel('data/UpDown.xlsm')  # adjust path if needed

    # ✅ Map actual Excel column names to expected names
    df.rename(columns={
        'Site Name': 'Facility',
        'Up/Down': 'Status',
        'Lat': 'Latitude',
        'Lon': 'Longitude'
    }, inplace=True)

    # Optional: Filter out rows missing coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Convert to list of dicts
    data = df.to_dict(orient='records')
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
