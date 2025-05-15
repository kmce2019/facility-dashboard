from flask import Flask, render_template
import pandas as pd
import requests

app = Flask(__name__)

def fetch_status(url):
    try:
        response = requests.get(url, timeout=5)
        return 200 if response.status_code == 200 else response.status_code
    except Exception:
        return 0  # Treat as down

@app.route('/')
def index():
    df = pd.read_excel('UpDown.xlsm')
    df['StatusCode'] = df['URL'].apply(fetch_status)
    df['Status'] = df['StatusCode'].apply(lambda x: 'UP' if x == 200 else 'DOWN')
    data = df.to_dict(orient='records')
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
