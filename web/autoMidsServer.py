from flask import Flask, request, jsonify, render_template
from autoMids import get_schedule, get_photos

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule')
def schedules():
    return render_template('schedule.html')

@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/freeperiods')
def freeperiods():
    return render_template('freeperiods.html')

if __name__ == "__main__":
    app.run(debug=True)