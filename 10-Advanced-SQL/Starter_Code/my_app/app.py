# Import the dependencies.
from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, text
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to the Hawaii Climate API!</h1><br/>"
        f"<h3>Available Routes:</h3><br/>"
        f"<a href='/api/v1.0/precipitation' target='_blank'>/api/v1.0/precipitation</a><br>"
        f"<a href='/api/v1.0/stations' target='_blank'>/api/v1.0/stations</a><br>"
        f"<a href='/api/v1.0/2017-08-23' target='_blank'>/api/v1.0/2017-08-23</a><br>"
        f"<a href='/api/v1.0/2017-08-01/2017-08-23' target='_blank'>/api/v1.0/2017-08-01/2017-08-23</a><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    # Using ORM
    db_data = session.query(Measurement.date, Measurement.station, Measurement.prcp).where(Measurement.date >= '2016-08-23').all()
    df2 = pd.DataFrame(db_data, columns=["date", "station", "prcp"])

    # turn into json
    data = df2.to_dict(orient="records")

    return jsonify(data)


@app.route("/api/v1.0/stations")
def stations():
    # USE RAW SQL
    query = """SELECT
                *
            FROM
                station;
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)


@app.route("/api/v1.0/<start>")
def date_start(start):
    # start is a date in the yyyy-mm-dd format
    print(start)

    # USE RAW SQL
    query = f"""SELECT
                min(tobs) as min_temp,
                avg(tobs) as avg_temp,
                max(tobs) as max_temp
            FROM
                measurement
            WHERE
                date >= '{start}';
            """
    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    # start/end is a date in the yyyy-mm-dd format
    print(start)
    print(end)

    # USE RAW SQL
    query = f"""SELECT
                min(tobs) as min_temp,
                avg(tobs) as avg_temp,
                max(tobs) as max_temp
            FROM
                measurement
            WHERE
                date >= '{start}'
                AND date <= '{end}';
            """
    print(query)

    df = pd.read_sql(text(query), con=engine)
    data = df.to_dict(orient="records")
    return jsonify(data)


#################################################
# Execute the App
#################################################
if __name__ == "__main__":
    app.run(debug=True)
