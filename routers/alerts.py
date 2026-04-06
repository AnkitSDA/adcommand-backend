from fastapi import APIRouter
from mock_data import ALERTS

router = APIRouter()

@router.get("/")
def get_alerts():
    """Return all alerts with summary counts."""
    counts = {"danger": 0, "warn": 0, "info": 0, "success": 0}
    for a in ALERTS:
        counts[a["type"]] += 1

    return {
        "summary": {
            "critical":    counts["danger"],
            "warnings":    counts["warn"],
            "opportunities": counts["info"],
            "resolved":    counts["success"],
        },
        "alerts": ALERTS
    }