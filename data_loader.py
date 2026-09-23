import csv
from database import SessionLocal
from models import Vehicle

def load_vehicles_from_csv(csv_file):
    """Load vehicles from a CSV file into the cargo database."""
    db = SessionLocal()
    with open(csv_file, newline='', encoding='utf-8') as vehicle_csvfile:
        reader = csv.DictReader(vehicle_csvfile)
        for row in reader:
            vehicle = Vehicle(
                vin=row['vin'],
                vrm=row['vrm'],
                colour=row['colour'],
                year=int(row['year']),
                make=row['make'],
                model=row['model'],
                branch=row['branch'],
                category=row['category'],
                fuel_kmpl=float(row['fuelEconomy']),
                seat_number=int(row['numberSeats']),
                daily_rate_gbp=float(row['dayRate']),
                status=row.get('status', 'AVAILABLE')
            )
            db.add(vehicle)
        db.commit()
    db.close()