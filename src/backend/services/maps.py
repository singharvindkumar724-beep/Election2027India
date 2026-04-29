import functools
from typing import Dict, Any, Union

@functools.lru_cache(maxsize=128)
def get_nearest_polling_station(zipcode: str) -> Dict[str, Any]:
    """
    Mock Google Maps JavaScript API / Geocoding integration.
    Uses lru_cache for efficiency to cache polling locations for the same zipcode.
    
    Args:
        zipcode (str): The zipcode to find the polling station for.
        
    Returns:
        Dict[str, Any]: A dictionary containing the status and polling station details.
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
    except Exception as e:
        return {"status": "error", "message": f"Maps API unreachable. Error: {str(e)}"}
