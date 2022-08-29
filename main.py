from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ready", methods = ['POST'])
def ready(): 
    if request.method == 'POST': #If the form has been submitted...
        f = request.files['file']
        f.save(secure_filename("uploaded" + f.filename))




if __name__ == '__main__':
    app.debug = True
    app.run()