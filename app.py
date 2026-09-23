from flask import Flask
from flask_jwt_extended import JWTManager
from database import engine, SessionLocal
from models import Base, Vehicle
from data_loader import load_vehicles_from_csv

app = Flask(__name__)
#creates and verifies JWT tokens
app.config["JWT_SECRET_KEY"] = "63090eb8c8186b068f08ca858f72ecceff56b138384d43ca58864c589b4c108e"
jwt = JWTManager(app)

@jwt.unauthorized_loader
def invalid_token_callback(error):
    return {
        "Error": "Authentication token is required. Please try again."
    }, 401
Base.metadata.create_all(bind=engine)

@app.teardown_appcontext
def remove_session(exception=None):
    SessionLocal.remove()

from routes.authorisation import * 
import routes.vehicles
import routes.search


if __name__ == "__main__":
    db = SessionLocal()
    if not db.query(Vehicle).first():
        load_vehicles_from_csv("data/vehicle.csv")
    db.close()
    app.run(debug=True)