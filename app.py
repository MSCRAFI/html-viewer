from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
import string
import random

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
allowed_extension = {'html', 'css'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in allowed_extension


@app.route('/')
def home():
    filelist = os.listdir(app.config['UPLOAD_FOLDER'])
    path = app.config['UPLOAD_FOLDER']
    return render_template("index.html", filelist=filelist, path=path)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filelist = os.listdir(app.config['UPLOAD_FOLDER'])
            if filename in filelist:
                print("Already Exist.")
                letters = string.ascii_lowercase
                rd_word = ''.join(random.choice(letters) for i in range(10))
                filename = rd_word + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return redirect("/")


# function to delete images
@app.route('/delete/<name>')
def method_name(name):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], name))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=10)
