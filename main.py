from flask import Flask, flash, render_template, request, send_file
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
        try:
            
            #ADDED: error msg when nothing is sent
            if f.filename == '':
                error = "No file submitted."
                
                return render_template("index.html", error = error)
            #To add: processing message / loading bar
            if f.filename.endswith(".csv") is False: 
                error = "The file submitted is not in a .csv format. Please try again."
                    
                return render_template("index.html", error = error)

            flash('File processed!')
        
            df = pd.read_csv(f)
            #df = geocode_df(df)    

            #To fix: adjust for geocoder timed out. maybe do manual geocoding?
            #To add: separate between submission and inserting the address yourself.
            
            file = secure_filename("testing" + ".csv") #Name goes here.
            df.to_csv(file, index = False)
            return render_template("index.html", tables = [df.to_html(classes = 'ul_table')], titles = [''], btn = "download.html")
        
        except Exception as e:
            return render_template("index.html", error = str(e))
            
#ADDED: 
# download function. technically this was the only req, but i wanna perfect this.       
# error message when file != csv.
# success msg.        


@app.route("/download")
def download():
    return send_file(file, as_attachment = True, download_name = "test.csv")

#Funct for geocoding using libraries. switch to manual geoc to avoid timeout error?
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