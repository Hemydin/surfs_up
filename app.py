# To import the Flask dependency, add the following to your code:
# from flask import Flask

# Add the following to your code to create a new Flask instance called app:
# app = Flask(__name__)

# Create Flask Routes:
# @app.route('/')

# Create a function called hello_world():
# @app.route('/')
# def hello_world():
#     return "Hello world"
# - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Set Up the Flask Weather App and import dependencies:
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies:
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import dependencies for Flask:
from flask import Flask, jsonify

# Set Up the Database
engine = create_engine("sqlite:///hawaii.sqlite")

# Relfect the database into our classes:
Base=automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table"
Measurement= Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database with the following code:
session = Session(engine)

# To define our Flask app, add the following line of code. This will create a Flask application called "app.":
app=Flask(__name__)

# We can define the welcome route using the code below:
@app.route("/")

# Add the precipitation, stations, tobs, and temp routes into our return statement.
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# To create the precipitation route:
@app.route("/api/v1.0/precipitation")

# Next, we will create the precipitation() function:
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Create the stations() route:
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create the temperature observation route:
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create the statistics route:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)