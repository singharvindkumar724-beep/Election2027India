import csv
import os
from typing import List, Dict, Any

def get_candidates() -> Dict[str, Any]:
    """
    Reads the candidates database. In a full production app, this would use the 
    Google Sheets API. To stay lightweight (<1MB), we read a CSV exported from Sheets.
    """
    candidates = []
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'candidates.csv')
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                candidates.append(row)
                
        return {
            "status": "live",
            "service": "Sheets (Local)",
            "data": {
                "candidates": candidates
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "service": "Sheets",
            "data": {
                "message": f"Failed to load candidates database: {str(e)}"
            }
        }
