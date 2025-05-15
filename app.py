from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    excel_path = os.path.join('data', 'UpDown.xlsm')
    df = pd.read_excel(excel_path)
    data = df.to_dict(orient='records')
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
