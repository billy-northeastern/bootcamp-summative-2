"""
Car-Go Rental API — Flask starter template (Flask + SQLAlchemy + SQLite)

YOUR TURN (marked "TODO" in the file, same pattern each time):
    GET    /vehicles/rented
    PATCH  /vehicles/<vrm>/rent
    PATCH  /vehicles/<vrm>/return
    POST   /vehicles
    DELETE /vehicles/<vrm>

STILL FULLY YOURS TO DESIGN (not scaffolded here at all):
    Your two chosen expansions.

Install first:
    pip install flask sqlalchemy

Run it:
    python cargo_api_starter_flask.py

"""

from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

# --- 1. Database connection ---
DATABASE_URL = "sqlite:///./cargo.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

class Vehicle(Base):
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String, primary_key=True, index=True)  # car registration number
    year = Column(String)
    make = Column(String)
    model = Column(String)
    branch = Column(String)
    fuel_efficiency_km_l = Column(Float)
    daily_rate_gbp = Column(Float)
    status = Column(String, default="AVAILABLE")  # RENTED / AVAILABLE / DAMAGED / SERVICEREQ

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.teardown_appcontext
def remove_session(exception=None):
    # Closes the DB session at the end of every request — Flask's rough
    # equivalent of what FastAPI's `Depends(get_db)` was doing for you
    # automatically before.
    SessionLocal.remove()

# --- 3. Manual serialisation helper ---
#     This is the bit Pydantic's response_model used to do for you —
#     in Flask, converting a DB row into JSON-ready data is your job.
def vehicle_to_dict(v):
    return {
        "vrm": v.vrm,
        "branch": v.branch,
        "fuel_efficiency_km_l": v.fuel_efficiency_km_l,
        "daily_rate_gbp": v.daily_rate_gbp,
        "status": v.status,
    }

# --- DONE: one specific vehicle ---
@app.route("/vehicles/<vrm>", methods=["GET"])
def get_vehicle(vrm):
    db = SessionLocal()
    vehicle = db.query(Vehicle).filter(Vehicle.vrm == vrm).first()
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle_to_dict(vehicle))

# --- DONE: all vehicles ---
@app.route("/vehicles", methods=["GET"])
def list_vehicles():
    db = SessionLocal()
    vehicles = db.query(Vehicle).all()
    return jsonify([vehicle_to_dict(v) for v in vehicles])

# --- DONE: available, grouped by branch ---
@app.route("/vehicles/available", methods=["GET"])
def available_vehicles():
    db = SessionLocal()
    vehicles = (db.query(Vehicle)
                  .filter(Vehicle.status == "AVAILABLE")
                  .order_by(Vehicle.branch)
                  .all())
    return jsonify([vehicle_to_dict(v) for v in vehicles])

# --- TODO: mirror available_vehicles() above, filter "RENTED" instead ---
@app.route("/vehicles/rented", methods=["GET"])
def rented_vehicles():
    return jsonify({"error": "Not implemented yet"}), 501

# --- TODO: look up the vehicle like get_vehicle() does, apply whichever
#     business rule you and your colleague agreed on for DAMAGED/SERVICEREQ/
#     already-RENTED vehicles, then vehicle.status = "RENTED"; db.commit() ---
@app.route("/vehicles/<vrm>/rent", methods=["PATCH"])
def rent_vehicle(vrm):
    return jsonify({"error": "Not implemented yet"}), 501

# --- TODO: mirror rent_vehicle() above, setting status back to "AVAILABLE" ---
@app.route("/vehicles/<vrm>/return", methods=["PATCH"])
def return_vehicle(vrm):
    return jsonify({"error": "Not implemented yet"}), 501

# --- TODO: this is the "hand-rolling validation" endpoint — no Pydantic
#     to check the incoming JSON for you anymore. Pull data = request.get_json(),
#     check the required fields yourself, build a Vehicle row, db.add()/commit() ---
@app.route("/vehicles", methods=["POST"])
def add_vehicle():
    return jsonify({"error": "Not implemented yet"}), 501

# --- TODO: look up the vehicle like get_vehicle() does, then
#     db.delete(vehicle) + db.commit() instead of returning it ---
@app.route("/vehicles/<vrm>", methods=["DELETE"])
def remove_vehicle(vrm):
    return jsonify({"error": "Not implemented yet"}), 501

# --- 4. Seed helper: same data as before, spanning all three branches ---
def seed_if_empty():
    db = SessionLocal()
    if not db.query(Vehicle).first():
        db.add_all([
            Vehicle(vrm="AB12CDE", branch="Manchester", fuel_efficiency_km_l=15.2,
                    daily_rate_gbp=35.0, status="AVAILABLE"),
            Vehicle(vrm="MC13FGH", branch="Manchester", fuel_efficiency_km_l=12.8,
                    daily_rate_gbp=42.0, status="RENTED"),
            Vehicle(vrm="BR14JKL", branch="Bristol", fuel_efficiency_km_l=18.5,
                    daily_rate_gbp=28.0, status="AVAILABLE"),
            Vehicle(vrm="BR15MNO", branch="Bristol", fuel_efficiency_km_l=14.0,
                    daily_rate_gbp=39.5, status="DAMAGED"),
            Vehicle(vrm="LU16PQR", branch="Luton", fuel_efficiency_km_l=16.7,
                    daily_rate_gbp=31.0, status="AVAILABLE"),
            Vehicle(vrm="LU17STU", branch="Luton", fuel_efficiency_km_l=13.3,
                    daily_rate_gbp=45.0, status="RENTED"),
        ])
        db.commit()
    db.close()

if __name__ == "__main__":
    seed_if_empty()
    app.run(debug=True)
