from fastapi import APIRouter, Query
from mock_data import CLIENTS

router = APIRouter()

def compute_roas(client):
    roas = round(client["revenue"] / client["spend"], 1) if client["spend"] else 0
    if roas >= 4:
        roas_class = "roas-good"
    elif roas >= 2.5:
        roas_class = "roas-medium"
    else:
        roas_class = "roas-low"
    return roas, roas_class

@router.get("/")
def get_all_clients(search: str = Query(default="")):
    """Return all clients, optionally filtered by search."""
    result = []
    for c in CLIENTS:
        if search.lower() in c["name"].lower() or search.lower() in c["type"].lower():
            roas, roas_class = compute_roas(c)
            result.append({**c, "roas": f"{roas}x", "roas_class": roas_class})
    return {"clients": result, "total": len(result)}

@router.get("/{client_id}")
def get_client(client_id: str):
    """Return a single client by ID."""
    for c in CLIENTS:
        if c["id"] == client_id.upper():
            roas, roas_class = compute_roas(c)
            return {**c, "roas": f"{roas}x", "roas_class": roas_class}
    return {"error": "Client not found"}

@router.get("/summary/stats")
def get_client_stats():
    """Summary numbers for the Clients page header."""
    active  = sum(1 for c in CLIENTS if c["status"] == "active")
    paused  = sum(1 for c in CLIENTS if c["status"] == "paused")
    warning = sum(1 for c in CLIENTS if c["status"] == "warning")
    total_spend = sum(c["spend"] for c in CLIENTS)
    return {
        "total":       len(CLIENTS),
        "active":      active,
        "paused":      paused,
        "warning":     warning,
        "total_spend": total_spend,
    }