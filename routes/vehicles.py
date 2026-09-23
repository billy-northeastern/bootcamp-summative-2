from flask import jsonify, request
from app import app
from database import SessionLocal
from models import Vehicle
from utility import vehicle_to_dict

# GET one specific vehicle
@app.route("/api/vehicles/<vrm>", methods=["GET"])
def get_vehicle(vrm):
    db = SessionLocal()

    vehicle = db.query(Vehicle).filter(Vehicle.vrm == vrm).first()
    #check if vehicle exists
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle_to_dict(vehicle))

# GET all vehicles
@app.route("/api/vehicles", methods=["GET"])
def list_vehicles():
    db = SessionLocal()
    # query for all vehicles
    vehicles = db.query(Vehicle).all()
    return jsonify([vehicle_to_dict(v) for v in vehicles])

# GET available vehicles
@app.route("/api/vehicles/available", methods=["GET"])
def available_vehicles():
    db = SessionLocal()
    # query for vehicles with status "AVAILABLE" and order by branch
    vehicles = (db.query(Vehicle)
                  .filter(Vehicle.status == "AVAILABLE")
                  .order_by(Vehicle.branch)
                  .all())
    return jsonify([vehicle_to_dict(v) for v in vehicles])

# GET rented vehicles
@app.route("/api/vehicles/rented", methods=["GET"])
def rented_vehicles():
    db = SessionLocal()
    # query for vehicles with status "RENTED" and order by branch
    vehicles = (db.query(Vehicle)
        .filter(Vehicle.status == "RENTED")
        .order_by(Vehicle.branch)
        .all()
    )

    return jsonify([vehicle_to_dict(v) for v in vehicles]
    )

# PATCH a vehicle to mark it as rented. 
@app.route("/api/vehicles/<vrm>/rent", methods=["PATCH"])
def rent_vehicle(vrm):

    db = SessionLocal()

    vehicle = db.query(Vehicle).filter(Vehicle.vrm == vrm).first()
    #check if vehicle exists and is available for rent
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    if vehicle.status != "AVAILABLE":
        return jsonify({"error": "Vehicle unavailable for rent"}), 400
    vehicle.status = "RENTED"

    db.commit()

    return jsonify(vehicle_to_dict(vehicle))

# PATCH a vehicle to mark it as returned. 
@app.route("/api/vehicles/<vrm>/return", methods=["PATCH"])
def return_vehicle(vrm):

    db = SessionLocal()
    vehicle = db.query(Vehicle).filter(Vehicle.vrm == vrm).first()
    #check if vehicle exists and is currently rented
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    if vehicle.status != "RENTED":
        return jsonify({"error": "Vehicle not currently rented"}), 400
    vehicle.status = "AVAILABLE"
    #apply changes 
    db.commit()
    return jsonify(vehicle_to_dict(vehicle))
     
# POST a new vehicle to the fleet. 
@app.route("/api/vehicles/add", methods=["POST"])
def add_vehicle():
    db = SessionLocal()
    data = request.get_json()

    # verify required fields are present
    required_fields = ["vin", "vrm", "colour", "year", "make", "model", "branch", "category", "seat_number", "daily_rate_gbp"]
    # validate all required fields are present in request data
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    #check if vehicle already present
    vehicle = db.query(Vehicle).filter(
        Vehicle.vrm == data["vrm"]
    ).first()
    if vehicle:
        return jsonify({"Error": "Vehicle already exists. Please try again."}), 400
    # create new vehicle
    vehicle = Vehicle(**data)
    db.add(vehicle)
    db.commit()

    return jsonify(vehicle_to_dict(vehicle)), 201


# DELETE a vehicle from the fleet. 
@app.route("/api/vehicles/<vrm>", methods=["DELETE"])
def remove_vehicle(vrm):
    db = SessionLocal()
    vehicle = db.query(Vehicle).filter(Vehicle.vrm == vrm).first()
    #check if vehicle exists
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    # delete vehicle from database
    db.delete(vehicle)
    db.commit()

    return jsonify({"message": "Vehicle removed successfully"}), 200
