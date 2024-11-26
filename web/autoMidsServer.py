import io
import os
import zipfile

from flask import Flask, render_template, request, send_file

from autoMidsBackend import get_photos, get_schedule

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule', methods=["POST"])
def schedules():
    alpha = request.form['alpha']
    result = get_schedule(alpha)
    return render_template('index.html', schedule=result)

@app.route('/photos', methods=["POST"])
def photos():
    company = request.form['company']
    year = request.form['year']
    photos = get_photos(company, year)
    return render_template('index.html', photos=photos[1], path=photos[0])

@app.route('/download_all/<path:dir_name>')
def download_all(dir_name):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        image_folder = os.path.join(app.static_folder, dir_name)
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            if os.path.isfile(file_path):
                zip_file.write(file_path, os.path.basename(file_path))

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name="images.zip")

@app.route('/freeperiods')
def freeperiods():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)