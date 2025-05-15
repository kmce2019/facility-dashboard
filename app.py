from flask import Flask, render_template
import pandas as pd
import requests
import concurrent.futures

app = Flask(__name__)

# Helper function to check a single URL
def check_url(url):
    try:
        response = requests.get(url, timeout=3)
        return 'UP' if response.status_code == 200 else 'DOWN', response.status_code
    except Exception:
        return 'DOWN', 0

# Fetches the data and performs concurrent status checks
def fetch_status_data():
    df = pd.read_excel('UpDown.xlsm')

    # Ensure Status and Status Code columns exist
    if 'Status' not in df.columns:
        df['Status'] = ''
    if 'Status Code' not in df.columns:
        df['Status Code'] = 0

    urls = df['URL'].tolist()

    # Run concurrent URL checks
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_url, urls))

    # Assign results back to DataFrame
    for index, (status, code) in enumerate(results):
        df.at[index, 'Status'] = status
        df.at[index, 'Status Code'] = code

    return df.to_dict(orient='records')

@app.route('/')
def index():
    data = fetch_status_data()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
