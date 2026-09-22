# Car-Go Connect API

This API is a monolithic web-service protoype for Car-Go's car rental booking and management platform, developed by XI Consulting to support the proposal for the tender. 


## Softare Setup
### Prerequisites 

```pip install -r requirements.txt```

Please ensure both vehicle.csv and customer.csv are in the data/ folder before running. 

* Python 3.9 or higher
* Flask 2.0 or higher
* pip
* virtualenv (optional but recommended)
* SQLite 3.0 or higher


### Technologies Used
**Python** - Object-Oriented Programming Language
**Flask** - Python web framework for building REST API and HTTP request handling
**Flask-SQLAlchemy** - Flask Extension connecting Python objects to database 
**SQLite** - Database for storing Car-Go data
**Postman** - Tests API through sending HTTP requests and verifying responses.
**VSCode** - Code editor for building. 

## Project Structure

CarGoRental/
├── app.py             # Flask app entry point, startup, route registration
├── models.py          # SQLAlchemy models (Vehicle, Customer)
├── database.py        # Database connection and session management
├── data_loader.py     # CSV data import into SQLite database
├── utility.py         # Helper function
├── routes/
│   ├── vehicles.py    # CRUD operations for vehicles + core rent/return endpoints
│   ├── search.py      # Cross-branch fleet search expansion
│   └── access.py      # RBAC / fleet summary report expansion
├── static/            # Static files i.e. HTML, CSS, JS
├── data/    
│   ├── vehicles.csv   # vehicle.csv, 
│   ├──customers.csv   #customer.csv
├── docs/
│   ├── postman_collection.json  # Exported Postman collection
│   └── supporting_documents     # Supporting documents
├── requirements.txt   # Project dependencies
└── .gitignore         # Git ignore file

## Installation

1. Clone the repository to your local machine.

git clone https://github.com/billy-northeastern/bootcamp-summative-2.git

cd your-repo-name

2. Create a virtual environment (optional but recommended).

Windows: 
```python -m venv venv```

```venv\Scripts\activate```

Mac/Linux:
```python3 -m venv venv```
```source venv/bin/activate```

3. Install the necessary dependencies.

```pip install -r requirements.txt```

4. Ensure the CSV files are in the data/ folder.

5. Run the application.

```python app.py```
6. The server will start running on the local web address https://127.0.0.1:5000. On first run, it loads all vehicles from the vehicle.csv file into a fresh SQLite database called **cargo.db**.


## Testing the API

A Postman collection covering all core endpoints below, with saved exmaples, is included in this submission (refer to /docs folder). All endpoints can also be tested via any HTTP client e.g. a web browser. 

## API Documentation

### Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET    | /api/vehicles/<vrm> | Information of one specific vehicle |
| GET    | /api/vehicles/<vrm> | Information of one specific vehicle |
| GET    | /api/vehicles | List all vehicles in the fleet |
| POST   | /api/vehicles | Add a new vehicle to the fleet |
| PATCH  | /api/vehicles/<vrm>/rent | Rent a vehicle (change status to RENTED) |
| PATCH  | /api/vehicles/<vrm>/return | Return a vehicle (change status to AVAILABLE) |
| DELETE | /api/vehicles/<vrm> | Remove a vehicle from the fleet |
| GET    | /api/vehicles/search | Search filter for vehicles by criteria |
|GET     | /api/report/fleet-summary | Fleet summary report (requires X-Staff-Role: management) |

## Validation Rules
**Rent**: fails with 400 if the vehicle's status is anything other than AVAILABLE.
**Return**: fails with 400 if the vehicle's status is anything other than RENTED.
**Add**: requires vin, vrm, colour, year, make, model, branch, category, seat_number, daily_rate_gbp; fails with 400 listing the missing field if any are missing.
**Fleet summary report**: requires the *X-Staff-Role: management* header; any other or missing value is rejected from viewing the report with a 403 error.

## Status (Error) Codes

|Code|Meaning|
|200|Success|
|201|New Vehicle Created|
|400|Invalid request|
|403|Unauthorised for this endpoint (role check failed)|
|404|Vehicle not found|

## Architecture Notes

### Layered Architecture 

Client (Frontend / Postman)
    ↓
[Flask API / Controller]
    - Handles HTTP requests
    - Basic input validation
    ↓
[Service]
    - Essential Business logic
    - Vehicle management
    - Cross-branch fleet search
    - Role-based staff access (RBAC)
    ↓
[Repository]
    - Handles database operations and data access
    - Uses SQLAlchemy
    ↓
[Model]
    - Defines Car-Go data structures 
    - SQLAlchemy models (maps classes into relational dbs)
    ↓
SQLite Database

### Initial Data Source

CSV Data
    ↓
Data Import
    ↓
SQLite Database

## Authors

Sameerah Mahmood - Backend Developer