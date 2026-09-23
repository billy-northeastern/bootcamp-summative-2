from flask import jsonify, request
from app import app
from database import SessionLocal
from models import Vehicle
from utility import vehicle_to_dict

#Expansion
# Search for vehicles based on optional filters (e.g. category, make, model, year, branch, number of seats, daily rate, status.)

@app.route("/api/vehicles/search", methods=["GET"])
def search_vehicles():
    db = SessionLocal()
    # define filters based on query parameters
    filters = {
        "category": Vehicle.category,
        "make": Vehicle.make,
        "model": Vehicle.model,
        "year": Vehicle.year,
        "branch": Vehicle.branch,
        "seat_number": Vehicle.seat_number,
        "daily_rate_gbp": Vehicle.daily_rate_gbp,
        "status": Vehicle.status,
        "fuel_kmpl": Vehicle.fuel_kmpl
    }

    #apply filters to the query based on provided parameters by user including category, rate, branch, fuel efficiency, and status.
    try:
        query = db.query(Vehicle)

        for param, column in filters.items():
            value = request.args.get(param)

            if value: 
                try:
                    if param in ["year", "seat_number"]:
                        value = int(value)
                    elif param in ["daily_rate_gbp", "fuel_kmpl"]:
                        value = float(value)
                    query = query.filter(column == value)
                except ValueError:
                    return jsonify({"Error": f"Incorrect value for {param}"}), 400

        vehicles = query.all()

        return jsonify([vehicle_to_dict(vehicle) for vehicle in vehicles]), 200
    
    finally:
        db.close()
