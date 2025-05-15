from flask import Flask, render_template
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
excel_file = "UpDown.xlsm"

def check_status(row):
    try:
        response = requests.get(row['URL'], timeout=5)
        status_code = response.status_code
        status = "UP" if status_code == 200 else "DOWN"
    except Exception:
        status_code = None
        status = "DOWN"
    row['Status'] = status
    row['Status Code'] = status_code
    return row

@app.route('/')
def index():
    df = pd.read_excel(excel_file)
    with ThreadPoolExecutor(max_workers=20) as executor:
        data = list(executor.map(check_status, df.to_dict(orient='records')))
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
