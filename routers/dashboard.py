from fastapi import APIRouter
from connectors.google_ads import get_manager_summary, get_account_performance, get_monthly_trend
from mock_data import CLIENTS, MONTHLY_TREND, CHANNEL_BREAKDOWN
import os

router = APIRouter()

def use_real_data():
    return bool(os.getenv("GOOGLE_ADS_REFRESH_TOKEN") and os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"))

@router.get("/summary")
def get_summary():
    if use_real_data():
        try:
            clients = get_manager_summary()
            total_spend = 0
            total_revenue = 0
            total_leads = 0
            for c in clients[:10]:
                perf = get_account_performance(c["id"], days=30)
                if perf:
                    total_spend += perf["total_spend"]
                    total_revenue += perf["total_revenue"]
                    total_leads += perf["total_conversions"]
            avg_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0
            return {
                "total_spend": round(total_spend),
                "total_revenue": round(total_revenue),
                "avg_roas": avg_roas,
                "total_leads": round(total_leads),
                "data_source": "Google Ads API",
                "changes": {"spend": "Live", "revenue": "Live", "roas": "Live", "leads": "Live"}
            }
        except Exception as e:
            print(f"Real data error, using mock: {e}")

    total_spend = sum(c["spend"] for c in CLIENTS)
    total_revenue = sum(c["revenue"] for c in CLIENTS)
    total_leads = sum(c["leads"] for c in CLIENTS)
    avg_roas = round(total_revenue / total_spend, 2) if total_spend else 0
    return {
        "total_spend": total_spend, "total_revenue": total_revenue,
        "avg_roas": avg_roas, "total_leads": total_leads,
        "data_source": "Mock Data",
        "changes": {"spend": "+8.2%", "revenue": "+14.5%", "roas": "+0.3x", "leads": "-2.1%"}
    }

@router.get("/trend")
def get_trend():
    if use_real_data():
        try:
            manager_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
            trend = get_monthly_trend(manager_id)
            if trend:
                return {"data": trend, "source": "live"}
        except Exception as e:
            print(f"Trend error: {e}")
    return {"data": MONTHLY_TREND, "source": "mock"}

@router.get("/channels")
def get_channels():
    return {"data": CHANNEL_BREAKDOWN}

@router.get("/clients-live")
def get_live_clients():
    if use_real_data():
        try:
            clients = get_manager_summary()
            return {"clients": clients, "total": len(clients), "source": "live"}
        except Exception as e:
            print(f"Live clients error: {e}")
    return {"clients": [], "source": "mock"}