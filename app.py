## Import flask instance
import datetime as dt
import numpy as np
import pandas as pd
#SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Flask dependencies
from flask import Flask, jsonify

#set up the Database
engine = create_engine("sqlite:///hawaii.sqlite")
#reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

#create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from Python to our database
session = Session(engine)

## Define Flask App 
### This __name__ variable denotes the name of the current function. You can use 
### the __name__ variable to determine if your code is being run from the 
### command line or if it has been imported into another piece of code. Variables
### with underscores before and after them are called magic methods in Python.
### For example, if we wanted to import our app.py file into another Python file named 
### example.py, the variable __name__ would be set to example
### However, when we run the script with python app.py, the __name__ variable will be set to __main__. 
### This indicates that we are not using any other file to run this code

app = Flask(__name__)

## Create Flask Routes
@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    #get the date and precipitation for the previous year. 
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   #create a dictionary with the date as the key and the precipitation as the value with jsonify (converts dictionary to JSON file)
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#We want to start by unraveling our results into a one-dimensional array.
#using np.ravel(), with results as our parameter.
#Next, we will convert our unraveled results into a list using list() function. 
# Then we'll jsonify the list and return it as JSON

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create a route to return the temperature observations for the previous year
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

