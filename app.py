from flask import Flask
from database import engine, SessionLocal
from models import Base, Vehicle
from data_loader import load_vehicles_from_csv

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

@app.teardown_appcontext
def remove_session(exception=None):
    SessionLocal.remove()

from routes.vehicles import *
from routes.search import *



if __name__ == "__main__":
    db = SessionLocal()
    if not db.query(Vehicle).first():
        load_vehicles_from_csv("data/vehicle.csv")
    db.close()
    app.run(debug=True)
