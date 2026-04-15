from google import genai
from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def analyze_contagion_risk(company_name, results):
    """
    Hyper-Speed Contagion Risk Analysis using Groq and Gemini Failover.
    """
    # Mock Ecosystem Generation
    debt = results.get("debt", 0)
    lenders = [
        {"name": "State Bank of India (SBI)", "exposure": round(debt * 0.4, 2)},
        {"name": "HDFC Bank", "exposure": round(debt * 0.3, 2)},
        {"name": "ICICI Bank", "exposure": round(debt * 0.3, 2)}
    ]
    related = [
        {"name": "Primary Steel Supplier (Sector A)", "type": "Supplier", "dependency": "High"},
        {"name": "Logistic Logistics Pvt Ltd", "type": "Service Provider", "dependency": "Medium"},
        {"name": "Automotive OEM Delta (Global)", "type": "Customer", "dependency": "Critical"}
    ]

    # 1. ATTEMPT PRIMARY: GROQ (Sub-second)
    if GROQ_API_KEY:
        try:
            print("DEBUG: Attempting Hyper-Speed Contagion Analysis with Groq")
            client = Groq(api_key=GROQ_API_KEY)
            prompt = f"""
You are an advanced banking risk system. Analyze contagion risk for:
1. Company: {company_name}
2. Financials: Revenue INR {results.get('revenue')} Cr, Debt INR {debt} Cr
3. Lenders: {json.dumps(lenders)}
4. Related Entities: {json.dumps(related)}

Return ONLY a JSON object:
"direct_impact": Text summary of lender impacts.
"indirect_impact": Text summary of supplier/customer impacts.
"systemic_risk": {{ "total_exposure": {debt}, "entities_affected": 6, "severity": "Localized/Moderate/Systemic" }}
"cascade_flow": List of failure steps.
"ai_verdict": 3-4 lines of professional conclusion.
"""
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            res_content = completion.choices[0].message.content
            if res_content:
                print("DEBUG: Groq Contagion Analysis Successful")
                data = json.loads(res_content)
                # Map systemic_risk to systemic_risk_summary for frontend compatibility
                return {
                    "direct_impact": data.get("direct_impact", ""),
                    "indirect_impact": data.get("indirect_impact", ""),
                    "systemic_risk_summary": data.get("systemic_risk", {}),
                    "cascade_flow": data.get("cascade_flow", []),
                    "ai_verdict": data.get("ai_verdict", "")
                }
        except Exception as e:
            print(f"DEBUG: Groq Contagion failed, failing over to Gemini: {e}")

    # 2. ATTEMPT FAILOVER: GEMINI (Tiered)
    if not GEMINI_API_KEY:
        return _get_fallback_contagion(company_name, results)

    models_to_try = [
        "gemini-2.0-flash", 
        "gemini-2.5-flash-lite", 
        "gemini-3-flash-preview"
    ]
    
    for model_name in models_to_try:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            print(f"DEBUG: Attempting Contagion Analysis with {model_name}")
            
            prompt = f"""
You are an advanced banking risk system. Analyze contagion risk for:
1. Company: {company_name}
2. Financials: Revenue INR {results.get('revenue')} Cr
3. Lenders: {json.dumps(lenders)}

Return JSON: "direct_impact", "indirect_impact", "systemic_risk", "cascade_flow", "ai_verdict".
"""
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            if response.text:
                print(f"DEBUG: Contagion Analysis successful via {model_name}")
                return json.loads(response.text)
        except Exception as e:
            print(f"DEBUG: Contagion Failover triggered for {model_name}: {e}")

    # 3. FINAL FALLBACK: DYNAMIC TEMPLATE
    print("WARNING: All AI Tiers Exhausted for Contagion. Using high-fidelity template.")
    return _get_fallback_contagion(company_name, results)

    return _get_fallback_contagion(company_name, results)

def _get_fallback_contagion(company_name, results):
    debt = results.get("debt", 0)
    return {
        "direct_impact": f"Concentrated exposure of INR {debt} Cr across State Bank of India and HDFC Bank. Potential for immediate provisioning requirement if default occurs.",
        "indirect_impact": f"Significant disruption to {company_name}'s supply chain. Critical dependency observed in Tier-1 automotive and logistics partners.",
        "systemic_risk": {
            "total_exposure": debt,
            "entities_affected": 8,
            "severity": "Moderate"
        },
        "cascade_flow": [
            "Primary default event at " + company_name,
            "Contraction of trade credit to related suppliers",
            "Heightened NPL risk for institutional lenders",
            "Secondary liquidity strain in regional steel ecosystem"
        ],
        "ai_verdict": f"The contagion profile for {company_name} suggests a localized but intense ripple effect. Professional oversight is required for the INR {debt} Cr exposure to prevent broader sectoral asset quality deterioration."
    }
