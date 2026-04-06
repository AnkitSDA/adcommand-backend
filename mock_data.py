"""
Mock data for Phase 2.
In Phase 3, each function here will be replaced with real API calls.
"""

CLIENTS = [
    {"id": "ZA", "name": "Zara Apparel",    "type": "E-commerce", "channels": "Google, Meta",   "spend": 320000, "budget": 350000, "revenue": 1984000, "leads": 820,  "status": "active"  },
    {"id": "NX", "name": "NexGen Tech",     "type": "SaaS",        "channels": "Google Ads",     "spend": 280000, "budget": 300000, "revenue": 1372000, "leads": 512,  "status": "active"  },
    {"id": "KF", "name": "Kiran Foods",     "type": "D2C Brand",   "channels": "Meta, CRM",      "spend": 210000, "budget": 200000, "revenue": 588000,  "leads": 640,  "status": "active"  },
    {"id": "VP", "name": "VitaPlus Health", "type": "Healthcare",  "channels": "Google Ads",     "spend": 190000, "budget": 180000, "revenue": 361000,  "leads": 290,  "status": "warning" },
    {"id": "SB", "name": "SkyBuild Infra",  "type": "Real Estate", "channels": "Google, Social", "spend": 140000, "budget": 150000, "revenue": 490000,  "leads": 180,  "status": "paused"  },
    {"id": "MG", "name": "MindGrow Edu",    "type": "EdTech",      "channels": "Meta, GA4",      "spend": 100000, "budget": 120000, "revenue": 310000,  "leads": 799,  "status": "active"  },
]

MONTHLY_TREND = [
    {"month": "Nov", "spend": 980000,  "revenue": 4200000},
    {"month": "Dec", "spend": 1120000, "revenue": 4800000},
    {"month": "Jan", "spend": 1050000, "revenue": 4400000},
    {"month": "Feb", "spend": 1090000, "revenue": 5000000},
    {"month": "Mar", "spend": 1140000, "revenue": 5100000},
    {"month": "Apr", "spend": 1240000, "revenue": 5810000},
]

CHANNEL_BREAKDOWN = [
    {"channel": "Google Ads",  "spend": 580000, "pct": 70},
    {"channel": "Meta Ads",    "spend": 410000, "pct": 50},
    {"channel": "GA4 Organic", "spend": 160000, "pct": 20},
    {"channel": "CRM / Email", "spend": 90000,  "pct": 11},
]

ALERTS = [
    {"type": "danger",  "title": "VitaPlus Health — ROAS dropped below 2x",         "desc": "ROAS fell from 3.1x to 1.9x in 7 days. Competitor bids increased on branded keywords.", "time": "2 hours ago",  "client": "VP"},
    {"type": "warn",    "title": "Kiran Foods — Budget 92% spent, 8 days left",     "desc": "At current burn rate, budget exhausts by April 9th. Pause low-performing ad sets.",    "time": "4 hours ago",  "client": "KF"},
    {"type": "warn",    "title": "Google Ads — Overpacing by 12%",                  "desc": "Total Google Ads spend tracking 12% above plan for April.",                             "time": "Yesterday",    "client": "ALL"},
    {"type": "info",    "title": "NexGen Tech — CTR increased by 34%",              "desc": "Ad creative B outperforming control by 34% CTR. Consider scaling budget.",              "time": "Yesterday",    "client": "NX"},
    {"type": "success", "title": "Zara Apparel — Best ROAS month ever (6.2x)",      "desc": "April tracking as best month. Revenue attribution up ₹12L vs March.",                  "time": "2 days ago",   "client": "ZA"},
    {"type": "info",    "title": "New keyword opportunity — 'affordable CRM India'", "desc": "High-intent, low-competition keyword found in NexGen Search Query Report.",            "time": "3 days ago",   "client": "NX"},
]