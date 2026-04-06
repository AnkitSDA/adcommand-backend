import os
from dotenv import load_dotenv
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

load_dotenv()

def get_google_ads_client():
    """Google Ads client banao credentials se."""
    credentials = {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),
        "use_proto_plus": True
    }
    return GoogleAdsClient.load_from_dict(credentials)


def get_all_client_accounts():
    """Manager account ke neeche saare client accounts lao."""
    try:
        client = get_google_ads_client()
        customer_service = client.get_service("CustomerService")
        accessible = customer_service.list_accessible_customers()
        
        accounts = []
        for resource_name in accessible.resource_names:
            customer_id = resource_name.split("/")[-1]
            accounts.append(customer_id)
        
        return accounts
    except GoogleAdsException as ex:
        print(f"Google Ads API Error: {ex}")
        return []


def get_account_performance(customer_id: str, days: int = 30):
    """Ek client account ki performance lao."""
    try:
        client = get_google_ads_client()
        ga_service = client.get_service("GoogleAdsService")

        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.all_conversions_value
            FROM campaign
            WHERE segments.date DURING LAST_{days}_DAYS
              AND campaign.status = 'ENABLED'
            ORDER BY metrics.cost_micros DESC
        """

        response = ga_service.search(customer_id=customer_id, query=query)

        campaigns = []
        total_spend = 0
        total_clicks = 0
        total_impressions = 0
        total_conversions = 0
        total_revenue = 0

        for row in response:
            spend = row.metrics.cost_micros / 1_000_000
            total_spend += spend
            total_clicks += row.metrics.clicks
            total_impressions += row.metrics.impressions
            total_conversions += row.metrics.conversions
            total_revenue += row.metrics.all_conversions_value

            campaigns.append({
                "id": row.campaign.id,
                "name": row.campaign.name,
                "spend": round(spend, 2),
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
                "conversions": row.metrics.conversions,
                "ctr": round((row.metrics.clicks / row.metrics.impressions * 100), 2) if row.metrics.impressions > 0 else 0,
                "cpc": round(spend / row.metrics.clicks, 2) if row.metrics.clicks > 0 else 0,
            })

        roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0

        return {
            "customer_id": customer_id,
            "total_spend": round(total_spend, 2),
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "total_conversions": total_conversions,
            "total_revenue": round(total_revenue, 2),
            "roas": roas,
            "campaigns": campaigns
        }

    except GoogleAdsException as ex:
        print(f"Error for account {customer_id}: {ex}")
        return None


def get_manager_summary():
    """Saare client accounts ka combined summary."""
    try:
        client = get_google_ads_client()
        ga_service = client.get_service("GoogleAdsService")
        manager_id = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")

        query = """
            SELECT
                customer_client.id,
                customer_client.descriptive_name,
                customer_client.currency_code,
                customer_client.manager,
                customer_client.status
            FROM customer_client
            WHERE customer_client.manager = False
              AND customer_client.status = 'ENABLED'
        """

        response = ga_service.search(customer_id=manager_id, query=query)

        clients = []
        for row in response:
            clients.append({
                "id": str(row.customer_client.id),
                "name": row.customer_client.descriptive_name,
                "currency": row.customer_client.currency_code,
                "status": "active"
            })

        return clients

    except GoogleAdsException as ex:
        print(f"Manager summary error: {ex}")
        return []


def get_monthly_trend(customer_id: str):
    """Last 6 months ka spend vs revenue trend."""
    try:
        client = get_google_ads_client()
        ga_service = client.get_service("GoogleAdsService")

        query = """
            SELECT
                segments.month,
                metrics.cost_micros,
                metrics.all_conversions_value
            FROM campaign
            WHERE segments.date DURING LAST_6_MONTHS
            ORDER BY segments.month ASC
        """

        response = ga_service.search(customer_id=customer_id, query=query)

        monthly = {}
        for row in response:
            month = row.segments.month[:7]
            if month not in monthly:
                monthly[month] = {"spend": 0, "revenue": 0}
            monthly[month]["spend"] += row.metrics.cost_micros / 1_000_000
            monthly[month]["revenue"] += row.metrics.all_conversions_value

        result = []
        for month, data in sorted(monthly.items()):
            result.append({
                "month": month,
                "spend": round(data["spend"], 2),
                "revenue": round(data["revenue"], 2)
            })

        return result

    except GoogleAdsException as ex:
        print(f"Trend error: {ex}")
        return []