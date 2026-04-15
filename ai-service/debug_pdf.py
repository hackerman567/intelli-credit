from cam_generator import generate_cam_report
import os

mock_financials = {
    "revenue": 150.5,
    "debt": 45.2,
    "profit": 12.8,
    "assets": 320.0,
    "meta": {"company_name": "RELIANCE RETAIL VENTURES - DEMO", "industry": "Consumer Retail"}
}

mock_risk = {
    "final_credit_score": 82,
    "risk_level": "LOW",
    "decision": "APPROVED",
    "explanation": "Strong market position and healthy cash flows support a positive credit outlook.",
    "ratios": {"dscr": 2.1, "debt_to_revenue": 30.0, "profit_margin": 8.5},
    "credit_notes": "The subject company EXHIBITS EXCELLENT REPAYMENT CAPACITY. Revenue has stabilized at 150Cr with a robust margin of 8.5%. The credit officer notes the strong parentage (Reliance Group) which provides an implicit sovereign-like guarantee. We recommend an immediate sanction of the requested limits with a review cycle of 12 months.",
    "validation_flags": ["Alpha Vantage revenue match verified"],
    "integrity_flags": ["Bank statement consistency 98%", "GST filing up-to-date"],
    "news_narrative": "The company has recently announced a major expansion in the Southern region, which is expected to boost top-line revenue by 15% in the next fiscal. No major legal or environmental liabilities were found in the current news audit cycle.",
    "news_flags": ["Positive Expansion News", "Stable Leadership"],
    "contagion": {
        "direct_impact": "Direct exposure of SBI (50Cr) and HDFC (30Cr) is well-collateralized.",
        "indirect_impact": "Positive spillover anticipated for local logistics partners and regional suppliers in the retail chain.",
        "cascade_flow": ["Revenue expansion starts", "Supplier order increase", "Local job creation", "Sectoral growth boost"],
        "ai_verdict": "Low contagion risk. The company acts as a stable anchor for its ecosystem."
    },
    "ews": {"ews_risk_level": "Low"},
    "ews_insight": "Early warning signals are dormant. No over-leveraging or inventory pile-up detected.",
    "suggested_limit": 500.0,
    "interest_rate": 8.25,
    "financial_insight": "Operating profits have grown by 15% CAGR over the last 3 years.",
    "promoter_insight": "Experienced board of directors with a clean track record in capital markets.",
    "meta": {"company_name": "RELIANCE RETAIL VENTURES - DEMO"}
}

output = "hackathon_detailed_demo.pdf"
try:
    print("Generating High-Density Professional PDF...")
    success = generate_cam_report(mock_financials, mock_risk, output)
    print(f"Success: {success}")
    if os.path.exists(output):
        print(f"File created: {output} ({os.path.getsize(output)} bytes)")
except Exception as e:
    import traceback
    print(f"CRASH DETECTED: {e}")
    print(traceback.format_exc())
