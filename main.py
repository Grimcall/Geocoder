from cgitb import text
from msilib.sequence import tables
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
import pandas as pd

app = Flask(__name__)
app.secret_key = "hellothere"
gloc = Nominatim(user_agent = "cross-geocoder")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods = ['POST'])
def ready(): 
    
    if request.method == 'POST': 
        f = request.files['f_address']
        
        #To add: error msg when nothing is sent
        if f.filename.endswith(".csv") is False: 
            error = "The file submitted is not in a .csv format. Please try again."
            
            return render_template("index.html", error = error)

        latitude = []
        longitude = []
       
       #Fix: This should flash as soon as the submission goes through, but it doesn't. It does so after the file is already processed, fix.
        flash('File submitted! Processing...')
       
        df = pd.read_csv(f)
        df.columns = df.columns.str.lower()
        df = df[['address']]
        
        for i in range(len(df)):   
            location = gloc.geocode(df.loc[i, 'address'])            
            latitude.append(location.latitude)
            longitude.append(location.longitude)

        df['latitude'] = latitude
        df['longitude'] = longitude

        #To add: separate between submission and inserting the address yourself.

        #To add: download function to finish 100%.
        #f.save(secure_filename("uploaded" + f.filename))

        
       
    return render_template("index.html", tables = [df.to_html(classes = 'ul_table')], titles = [''])

if __name__ == '__main__':
    app.debug = True
    app.run()