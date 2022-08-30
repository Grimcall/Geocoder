from cgitb import text
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas

app = Flask(__name__)
app.secret_key = "yuhyeet"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def ready(): 
    if request.method == 'POST': #If the form has been submitted...
        f = request.files['f_address']
        
        if f.filename.endswith(".csv") is False: #If file submitted is not csv...
            error = "The file submitted is not in a .csv format. Please try again."
            
            return render_template("index.html", error = error)
        
        flash('File submitted! Processing...')
        f.save(secure_filename("uploaded" + f.filename))
        
        print(f.filename)
        print(f)
        print(type(f))
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.debug = True
    app.run()