# web-app for API image manipulation

from flask import Flask, request, render_template, send_from_directory, send_file
import os
from PIL import Image
import plat
from zipfile import ZipFile

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
plat_br = ('now', 'sky', 'google', 'vivo')
plat = {
    'google': (2000, 3000),
    'sky': (1000, 1500),
    'vivo': (600, 882),
    'now': (220, 340),

}


# default access page
@app.route("/")
def main():
    return render_template('index.html')


# upload selected image and forward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/images/')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from html file-picker
    upload = request.files.getlist("file")[0]
    print("File name: {}".format(upload.filename))
    
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".png") or (ext == ".bmp"):
        print("File accepted")
    else:
        return render_template("error.html", message="The selected file is not supported"), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)

    # forward to processing page
    return render_template("processing.html", image_name=filename)


# now filename the specified degrees
@app.route("/now", methods=["POST"])
def now():
    # retrieve parameters from html form
    # angle = request.form['angle']
    filename = request.form['image']

    # open and process image
    target = os.path.join(APP_ROOT, 'static/images')
    destination = "/".join([target, filename])
    poster = destination
    # create a ZipFile object
    zipobj = ZipFile(target + '/' + filename[:-4] + '.zip', 'w')
    for c in plat_br:
        plat_size = plat[c]
        img = Image.open(poster)
        img = img.resize(plat_size, Image.ANTIALIAS)
        # save and return image
        destination = "/".join([target, c + '_' + filename])
        if os.path.isfile(destination):
            os.remove(destination)
        img.save(destination)
        # Add multiple files to the zip
        zipobj.write(destination, c + '_' + filename)

    print(target + '/' + filename[:-4] + '.zip')

    # close the Zip File
    zipobj.close()

    return send_file(target + '/' + filename[:-4] + '.zip')

    # img = Image.open(destination)
    # img = img.resize(plat.now, Image.ANTIALIAS)

    # save and return image
    # destination = "/".join([target, 'temp.jpg'])
    # if os.path.isfile(destination):
    #     os.remove(destination)
    # img.save(destination)
    #
    # return send_image('temp.png')


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("static/images", filename)


if __name__ == "__main__":
    app.run()
