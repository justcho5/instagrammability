#!/usr/bin/env python
from flask import Flask, request, redirect, render_template, send_from_directory
import jinja2.exceptions
from werkzeug.utils import secure_filename
from keras.models import load_model
import os
import sys
import base64
import time


sys.path.insert(
    0,
    "./create_model/scripts/"
)
from images import convert_images, crop

# UPLOAD_FOLDER = '/home/justina/Desktop/instagrammability/data/uploaded/original/'
# UPLOAD_FOLDER = '/Users/mike/Documents/upload/'
UPLOAD_FOLDER = "./create_model/images/uploaded/original/"


# initialize Flask application and the Keras model
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config.update(DEBUG=True)

model = load_model(
    "./create_model/models/model.hdf5"
)
model._make_predict_function()
print("Model loaded. Start serving...")


@app.route("/")
def index():
    return render_template("index.html")


def do_prediction(filename):
    new_path = crop(UPLOAD_FOLDER, filename)

    x_test = convert_images([new_path], 3, 224, 224, "resnet50")
    pred = model.predict(x_test)[0][0] * 100
    # pred = "%.1f" % pred
    pred = int(round(pred))
    return pred


@app.route("/score", methods=["POST"])
def score():
    f = request.form.get("file").split(",")[1]
    imgdata = base64.b64decode(f)
    millis = int(round(time.time() * 1000))
    filename = "some_image_" + str(millis) + ".png"
    with open(UPLOAD_FOLDER+filename, "wb") as f:
        f.write(imgdata)
    print("Image uploaded.")
    pred = do_prediction(filename)

    return render_template("index.html", label=pred)


@app.route("/predict", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == "":
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            pred = do_prediction(filename)
            return render_template("index.html", label=pred)


@app.route("/<pagename>")
def admin(pagename):
    return render_template(pagename + ".html")


@app.route("/<path:resource>")
def serveStaticResource(resource):
    return send_from_directory("static/", resource)


@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)


@app.errorhandler(404)
def not_found(e):
    return "<strong>Page Not Found!</strong>", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
