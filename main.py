from cgitb import text
from msilib.schema import File
from msilib.sequence import tables
from flask import Flask, flash, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim
import pandas as pd

app = Flask(__name__)
app.secret_key = "hellothere"
gloc = Nominatim(user_agent = "cross-geocoder")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-table", methods = ['POST'])
def process(): 
    global file
    if request.method == 'POST': 
        f = request.files['f_address']
        
        #To add: error msg when nothing is sent
        if f.filename.endswith(".csv") is False: 
           error = "The file submitted is not in a .csv format. Please try again."
            
           return render_template("index.html", error = error)

       #Fix: This should flash as soon as the submission goes through, but it doesn't. It does so after the file is already processed, fix.
        flash('File submitted! Processing...')
       
        df = pd.read_csv(f)
        #df = geocode_df(df)    

        #To add: separate between submission and inserting the address yourself.
        

        file = "testing" + ".csv"
        df.to_csv(file, index = False)
        #file.save(f.filename)

        #ADDED: download function to finish 100%. Shows a type error, but we can fix it later.
        
        print(f)
        
        return render_template("index.html", tables = [df.to_html(classes = 'ul_table')], titles = [''], btn = "download.html")
  

@app.route("/download")
def download():
    return send_file(file, as_attachment = True, download_name = "test.csv")

def geocode_df(dataframe):
    latitude = []
    longitude = []
    
    dataframe.columns = dataframe.columns.str.lower()
    
    dataframe = dataframe[['address']]
        
    for i in range(len(dataframe)):   
        location = gloc.geocode(dataframe.loc[i, 'address'])            
        latitude.append(location.latitude)
        longitude.append(location.longitude)

    dataframe['latitude'] = latitude
    dataframe['longitude'] = longitude

    return dataframe


if __name__ == '__main__':
    app.debug = True
    app.run()