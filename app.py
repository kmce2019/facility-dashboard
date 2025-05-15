from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df = pd.read_excel('data/UpDown.xlsm')

    # Normalize column names
    df.rename(columns={
        'Site Name': 'Facility',
        'Up/Down': 'Status',
        'Lat': 'Latitude',
        'Lon': 'Longitude'
    }, inplace=True)

    # Coerce coordinates to numeric
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    # Drop rows with invalid coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Print debug info to verify
    data = df.to_dict(orient='records')
    print("DEBUG DATA >>>", data)

    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
