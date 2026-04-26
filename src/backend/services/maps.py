def get_nearest_polling_station(zipcode):
    """
    Mock Google Maps JavaScript API / Geocoding integration.
    """
    try:
        return {
            "status": "success",
            "station": {
                "name": f"Community Center Booth for {zipcode}",
                "address": f"123 Main St, Region {zipcode}",
                "accessible": True,
                "lat": 28.6139,
                "lng": 77.2090
            }
        }
    except Exception:
        return {"status": "error", "message": "Maps API unreachable."}
