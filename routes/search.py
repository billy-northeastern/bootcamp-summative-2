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
    query = db.query(Vehicle)
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
    #apply filters to the query based on provided parameters by user
    for param, column in filters.items():
        value = request.args.get(param)
        if value:
            query = query.filter(column == value)
    vehicles = query.all()
    #return filtered vehicles as JSON response
    return jsonify([vehicle_to_dict(vehicle) for vehicle in vehicles])
