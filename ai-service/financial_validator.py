import os
import requests
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

def validate_financials(company_name, extracted_revenue):
    """
    Fetches benchmark financial data and cross-validates extracted revenue.
    """
    if not ALPHA_VANTAGE_KEY:
        return 0, ["Alpha Vantage Key missing (Skipping external validation)"]

    try:
        # Note: Using SYMBOL search first would be ideal, but for demo we use a generic search
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={ALPHA_VANTAGE_KEY}"
        search_res = requests.get(url, timeout=5).json()
        matches = search_res.get('bestMatches', [])
        
        if not matches:
            return 0, []

        symbol = matches[0].get('1. symbol')
        
        # Fetch Income Statement for revenue validation
        inc_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
        inc_res = requests.get(inc_url, timeout=5).json()
        
        annual_reports = inc_res.get('annualReports', [])
        if not annual_reports:
            return 0, []

        # Compare with latest annual revenue (assuming data is in same unit order)
        latest_rev = float(annual_reports[0].get('totalRevenue', 0)) / 10**7 # Convert to INR Crore approx if needed
        
        # Simple tolerance check (20%)
        diff = abs(extracted_revenue - latest_rev)
        if diff > (latest_rev * 0.2):
            return -10, [f"Financial Inconsistency: Extracted revenue ({extracted_revenue} Cr) significantly differs from benchmark ({round(latest_rev, 2)} Cr)"]

        return 0, []

    except Exception as e:
        print(f"Alpha Vantage error: {e}")
        return 0, []
