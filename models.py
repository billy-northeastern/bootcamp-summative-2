from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base

# base class for defining database models e.g. Vehicle
Base = declarative_base()

class Vehicle(Base):
    """Database model for a vehicle in the CarGo rental fleet."""
    __tablename__ = "vehicles"
    vehicle_id = Column(Integer, primary_key=True, autoincrement=True)
    vin = Column(String,unique=True, index=True)  # vehicle identification number
    year = Column(Integer) 
    vrm = Column(String, unique=True, index=True)  # vehicle registration mark
    make = Column(String)
    colour = Column(String)
    model = Column(String)
    branch = Column(String) # branch location of vehicle
    category = Column(String) # type of vehicle
    fuel_kmpl = Column(Float) # fuel economy in km per litre
    seat_number = Column(Integer) 
    daily_rate_gbp = Column(Float) # rental cost per day
    status = Column(String, default="AVAILABLE")  # status of vehicle (AVAILABLE, RENTED, MAINTENANCE)

