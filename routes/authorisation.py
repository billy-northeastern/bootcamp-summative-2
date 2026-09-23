from functools import wraps
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import request, jsonify
from models import Vehicle
from app import app
from database import SessionLocal

# hardedcoded user credentials for demonstration purposes. 
# Real applications should use a secure database and hashed passwords.

USER_ROLES = {
    "management": {"password": "management123", "role": "management"}
}
def require_role(role):
    """Decorator used to restrict access to API routes based on user role"""
    def decorator(f):
        @wraps(f) 
        @jwt_required()
        def decorated_function(*args, **kwargs):
            claims = get_jwt()
            # decline access if the user's role does not align with required role
            if claims.get("role") != role:
                return jsonify({"Error": "Access denied. Insufficient permissions."}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# authenticates a user, returning JWT access token when credentials are correct
@app.route('/api/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = USER_ROLES.get(username)
    if not user or user["password"] != password:
        return jsonify({"Error": "Incorrect username or password"}), 401
    token = create_access_token(identity=username, additional_claims={"role": user["role"]})
    return jsonify({"access_token": token}), 200

# generates a fleet summary report that requires management authorisation first
@app.route('/api/report/fleet-summary', methods=['GET'])
@require_role('management')
def fleet_summary():
    db = SessionLocal()
    # get a list of all unique branches in database
    branches = db.query(Vehicle.branch).distinct().all()

    fleet_summary = []
    # create statistics for each branch
    for row in branches:
        branch = row[0]

        #Get all vehicles from the current branch 
        vehicles = db.query(Vehicle).filter(Vehicle.branch == branch).all()

        # Count total number of vehicles in the branch 
        total_vehicles = len(vehicles)
        # Count all rented vehicles 
        rented_vehicles = 0
        for v in vehicles:
            if v.status == "RENTED":
                rented_vehicles += 1
        # compute utilisation rate of each branch i.e. how many vehicles are RENTED
        utilisation_rate = 0

        if total_vehicles > 0:
            utilisation_rate = (rented_vehicles / total_vehicles) * 100

        fleet_summary.append({
            "branch": branch,
            "total_vehicles": total_vehicles,
            "rented_vehicles" : rented_vehicles,
            "utilisation_rate_pc" : f"{round(utilisation_rate)}%"
        })
   
    db.close()
    return jsonify(fleet_summary), 200
