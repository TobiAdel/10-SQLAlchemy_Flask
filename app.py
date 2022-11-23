#imports
from flask import Flask, jsonify
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#Create an app
app = Flask(__name__)

#Home Page
@app.route("/")
def home():

    print("Server received request for 'Home' page...")
#add the format date to code
    """List all available api routes."""
    return (
        f"<h1>Hawaii Climate App</h1><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/&lt;start&gt;</br>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"  
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    

    """precipitation analysis last 12 months."""
    n = 365
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    datetime_str = recent_date.date
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
    past_date = datetime_obj - relativedelta(days=n)
    meas_prcp = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= past_date).all()

    m_prcp = []
    for date, prcp, in meas_prcp:
        measure_prcp = {}
        measure_prcp["date"] = date
        measure_prcp["prcp"] = prcp
        m_prcp.append(measure_prcp)

    

    return jsonify(m_prcp)

@app.route("/api/v1.0/stations")
def stations():
    

    hawaii_stations = session.query(Station.station, Station.name).all()
    all_stations = list(np.ravel(hawaii_stations))

    

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
   

    """precipitation analysis last 12 months."""
    n = 365
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    datetime_str = recent_date.date
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
    past_date = datetime_obj - relativedelta(days=n)

    st_tobs = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= past_date).all()
    testing = list(np.ravel(st_tobs))

    return jsonify(testing)

@app.route("/api/v1.0/<start>")
def start(start):

    meas_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    testing1 = list(np.ravel(meas_temp))

    return jsonify(testing1)



@app.route("/api/v1.0/<start>/<end>")
def date_range(start,end):

    meas_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    testing2 = list(np.ravel(meas_temp))

    return jsonify(testing2)

if __name__ == "__main__":
       app.run(debug=True)


