def vehicle_to_dict(v):
    return {
        "vehicle_id": v.vehicle_id,
        "make": v.make,
        "model": v.model,
        "colour": v.colour,
        "year": v.year,
        "vin": v.vin,
        "vrm": v.vrm,
        "branch": v.branch,
        "category": v.category,
        "seat_number": v.seat_number,
        "fuel_kmpl": v.fuel_kmpl,
        "daily_rate_gbp": v.daily_rate_gbp,
        "status": v.status
    }