from flask import Flask, request, jsonify, render_template
from autoMidsBackend import get_schedule, get_photos

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule', methods=["POST"])
def schedules():
    alpha = request.form['alpha']
    result = get_schedule(alpha)
    return render_template('index.html', schedule=result)

@app.route('/photos')
def photos():
    return render_template('index.html')

@app.route('/freeperiods')
def freeperiods():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)