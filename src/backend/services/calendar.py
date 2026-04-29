import functools
from typing import Dict, Any, List

@functools.lru_cache(maxsize=1)
def get_election_timeline() -> Dict[str, Any]:
    """
    Mock Google Calendar API integration for election phases.
    Uses lru_cache to cache the election timeline since it doesn't change frequently.
    
    Returns:
        Dict[str, Any]: A dictionary containing the status and a list of election phases.
    """
    try:
        phases: List[Dict[str, Any]] = [
            {"phase": 1, "date": "2027-04-11", "regions": ["Delhi", "Haryana"]},
            {"phase": 2, "date": "2027-04-18", "regions": ["Maharashtra", "Karnataka"]}
        ]
        return {
            "status": "success",
            "phases": phases
        }
    except Exception as e:
        return {"status": "error", "message": f"Calendar API unreachable. Error: {str(e)}"}
