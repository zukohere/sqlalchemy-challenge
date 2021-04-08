# # 1. import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# added import inspector
from sqlalchemy import inspect
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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
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


# * `/api/v1.0/tobs`
#   * Query the dates and temperature observations of the most active station for the last year of data.

#   * Return a JSON list of temperature observations (TOBS) for the previous year.

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
if __name__ == '__main__':
    app.run(debug=True)