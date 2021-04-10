# # 1. import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# added import inspector
from sqlalchemy import inspect, and_
#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
import sqlite3
engine = create_engine("sqlite:///Step_1_Climate_Analysis_And_Exploration/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
inspector = inspect(engine)
for table in inspector.get_table_names():
    vars()[table.title()] = Base.classes[table]


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("---Home page----<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"dates in the form YYYY-MM-DD"
    )
@app.route("/api/v1.0/precipitation")
def precip():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        all_precip.append(precip_dict)
    # Return the JSON representation of your dictionary.
    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def station_list():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    # Return a JSON list of stations from the dataset.
    all_names = list(np.ravel(results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def active_station_data():
    session = Session(engine)
    # List the stations and the counts in descending order to obtain most active station
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)\
                                .order_by(func.count(Measurement.station).desc()).all()
    most_active_st = active_stations[0][0]
    # * Query the dates and temperature observations of the most active station for the last year of data.
    active_st_temps_query=session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_st).filter(Measurement.date >= "2016-08-23").all()
    session.close()
#   * Return a JSON list of temperature observations (TOBS) for the previous year.
    list_dict_active_station_temps = []
    for date, temp in active_st_temps_query:
        active_st_dict = {}
        active_st_dict[date]=temp
        list_dict_active_station_temps.append(active_st_dict)
    return jsonify(list_dict_active_station_temps)   
@app.route("/api/v1.0/<sdate>")
def start_only(sdate):
    session = Session(engine)
    start_end_query = session.query(Measurement.tobs).filter(Measurement.date >= sdate).all()
    session.close()
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    list_start_end_query = [result[0] for result in start_end_query]
    list_dict_start_end = []
    start_end_dict = {}
    start_end_dict["TMIN"]=round(min(list_start_end_query),2)
    start_end_dict["TAVG"]=round(sum(list_start_end_query)/len(list_start_end_query),2)
    start_end_dict["TMAX"]=round(max(list_start_end_query),2)
    list_dict_start_end.append(start_end_dict)
    return jsonify(list_dict_start_end)

@app.route("/api/v1.0/<sdate>/<edate>")
def date_range(sdate,edate):
    session = Session(engine)
    start_end_query = session.query(Measurement.tobs).filter(and_(Measurement.date >= sdate, Measurement.date <= edate)).all()
    session.close()
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    list_start_end_query = [result[0] for result in start_end_query]
    list_dict_start_end = []
    start_end_dict = {}
    start_end_dict["TMIN"]=round(min(list_start_end_query),2)
    start_end_dict["TAVG"]=round(sum(list_start_end_query)/len(list_start_end_query),2)
    start_end_dict["TMAX"]=round(max(list_start_end_query),2)
    list_dict_start_end.append(start_end_dict)
    return jsonify(list_dict_start_end)

if __name__ == '__main__':
    app.run(debug=True)