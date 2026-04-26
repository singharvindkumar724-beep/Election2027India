def get_election_timeline():
    """
    Mock Google Calendar API integration for election phases.
    """
    try:
        return {
            "status": "success",
            "phases": [
                {"phase": 1, "date": "2027-04-11", "regions": ["Delhi", "Haryana"]},
                {"phase": 2, "date": "2027-04-18", "regions": ["Maharashtra", "Karnataka"]}
            ]
        }
    except Exception as e:
        return {"status": "error", "message": "Calendar API unreachable."}
