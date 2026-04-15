import time
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from pdf_parser import extract_financial_data
from risk_engine import calculate_risk_score, get_risk_level, get_composite_risk_score
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from cam_generator import generate_cam_report
from news_risk_analyzer import analyze_news
from financial_integrity import financial_integrity_check
from promoter_risk import evaluate_promoter_risk
from liquidity_engine import analyze_liquidity_stress
from ews_engine import analyze_ews
from credit_notes_generator import generate_credit_notes
from financial_ratios import calculate_ratios
from financial_validator import validate_financials
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Intelli-Credit AI Service")

# Correcting paths to point to the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "backend", "uploads")
REPORT_DIR = os.path.join(BASE_DIR, "backend", "reports")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

class AnalysisRequest(BaseModel):
    filename: str
    company_name: str
    promoter_name: str = "Rajesh Sharma"
    officer_notes: str = ""
    sector: str = "Manufacturing"

class SimulationRequest(BaseModel):
    revenue: float
    debt: float
    profit: float
    assets: float
    promoter_score: float = 70.0
    liquidity_score: float = 70.0
    officer_sentiment: int = 0

@app.post("/analyze")
async def analyze_pdf(request: AnalysisRequest):
    print(f"DEBUG: Received Analysis Request for {request.company_name} - {request.filename}")
    try:
        start_time = time.time()
        pdf_path = os.path.join(UPLOAD_DIR, request.filename)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"PDF file not found at {pdf_path}")
        
        # 1. Process PDF for base financials
        financials = extract_financial_data(pdf_path)
        revenue = financials.get("revenue", 0)
        
        # 2. Advanced Metrics (Phase 6)
        ratios = calculate_ratios(financials)
        
        # 3. External Financial Validation (Alpha Vantage)
        val_penalty, val_flags = validate_financials(request.company_name, revenue)
        
        # 4. Sentiment Analysis of Officer Notes
        # A simple keyword check for demo purposes (HACKATHON PILLAR 2)
        officer_sentiment = 0
        if "strong" in request.officer_notes.lower() or "modern" in request.officer_notes.lower():
            officer_sentiment = 1
        elif "weak" in request.officer_notes.lower() or "low capacity" in request.officer_notes.lower():
            officer_sentiment = -1
        
        # 4. News & Reputation Risk (Enhanced)
        news_penalty, news_flags, news_level, news_narrative = analyze_news(request.company_name)
        has_news_risk = (news_penalty < 0)
        
        # 5. Financial Integrity
        int_dataset = {
            "revenue": revenue,
            "bank_inflow": revenue * 0.65, 
            "gst_sales": revenue * 0.7     
        }
        integrity_penalty, integrity_flags = financial_integrity_check(int_dataset)
        
        # 6. Promoter Governance
        mock_profile = {
            "total_companies": 6,
            "closed_companies": 2,
            "legal_cases": 1,
            "active_companies": 4
        }
        promoter_results = evaluate_promoter_risk(request.promoter_name, mock_profile)
        
        # 7. Liquidity Stress
        liquidity_results = analyze_liquidity_stress(financials)
        
        # 8. Early Warning System (Enhanced)
        ews_results = analyze_ews(
            calculate_risk_score(financials), 
            liquidity_results["liquidity_score"], 
            promoter_results["promoter_risk_score"],
            news_risk=has_news_risk,
            extra_data=liquidity_results
        )
        
        # 8.5 Graph Intelligence Scan (Forensic DNA Check)
        from graph_engine import check_network_risk
        graph_results = check_network_risk(
            request.promoter_name, 
            request.company_name, 
            financials.get("location", "India")
        )
        network_flags = graph_results["network_flags"]
        network_penalty = graph_results["network_penalty"]

        # 9. FIVE Cs BANKING SCORING
        from risk_engine import calculate_five_cs, get_composite_risk_score, calculate_loan_recommendation
        
        pillar_scores = calculate_five_cs(
            financials, 
            ratios, 
            promoter_results, 
            news_penalty, 
            officer_sentiment=officer_sentiment,
            network_penalty=network_penalty
        )
        
        final_score, final_risk_level = get_composite_risk_score(pillar_scores)
        
        # Decision (Pillar 3: Recommendation Engine)
        decision, explanation, suggested_limit, interest_rate = calculate_loan_recommendation(final_score, revenue)
        
        # 10. AI Credit Officer Notes (Gemini API)
        dossier = {
            "company_name": request.company_name,
            "pillar_scores": pillar_scores,
            "financial_score": final_score,
            "promoter_score": pillar_scores.get('character', 50),
            "dscr": ratios.get("dscr"),
            "profit_margin": ratios.get("profit_margin"),
            "debt_to_revenue": ratios.get("debt_to_revenue"),
            "liquidity_score": liquidity_results["liquidity_score"],
            "ews_risk_level": ews_results["ews_risk_level"],
            "news_narrative": news_narrative,
            "risk_level": final_risk_level,
            "risk_flags": integrity_flags + news_flags + val_flags + network_flags
        }
        notes_results = generate_credit_notes(dossier)
        
        processing_time = round(time.time() - start_time, 2)
        
        # Combine results
        results = {
            **financials,
            "final_credit_score": final_score,
            "risk_level": final_risk_level,
            "pillar_scores": pillar_scores,
            "liquidity_risk": liquidity_results,
            "promoter_risk": promoter_results,
            "network_flags": network_flags,
            "news_flags": news_flags,
            "news_level": news_level,
            "news_narrative": news_narrative,
            "validation_flags": val_flags,
            "integrity_flags": integrity_flags,
            "ratios": ratios,
            "ews": ews_results,
            "credit_notes": notes_results.get("credit_officer_notes", ""),
            "financial_insight": notes_results.get("financial_insight", ""),
            "promoter_insight": notes_results.get("promoter_insight", ""),
            "liquidity_insight": notes_results.get("liquidity_insight", ""),
            "ews_insight": notes_results.get("ews_insight", ""),
            "reputation_insight": notes_results.get("reputation_insight", ""),
            "decision": decision,
            "explanation": explanation,
            "suggested_limit": suggested_limit,
            "interest_rate": interest_rate,
            "officer_sentiment": officer_sentiment,
            "metrics": {
                "docs": 1,
                "engines": 10,
                "time": processing_time
            },
            "meta": {
                "company_name": request.company_name,
                "industry": request.sector,
                "location": financials.get("location", "India"),
                "year": financials.get("year", "2012")
            }
        }
        
        # 11. CONTAGION RISK ANALYSIS (Systemic Ripple Effect)
        from contagion_analyzer import analyze_contagion_risk
        contagion_results = analyze_contagion_risk(request.company_name, results)
        results["contagion"] = contagion_results

        app.state.last_analysis = results
        return results
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in analyze_pdf: {error_details}")
        raise HTTPException(status_code=500, detail=f"Internal Analysis Error: {str(e)}")

@app.post("/simulate")
async def simulate_credit(request: SimulationRequest):
    try:
        # Re-use existing business logic
        from risk_engine import calculate_risk_score, get_risk_level, get_composite_risk_score, calculate_loan_recommendation
        
        financials = {
            "revenue": request.revenue,
            "debt": request.debt,
            "profit": request.profit,
            "assets": request.assets
        }
        
        financial_score = calculate_risk_score(financials)
        composite_score, risk_level = get_composite_risk_score(
            financial_score, 
            request.liquidity_score, 
            request.promoter_score,
            officer_sentiment=request.officer_sentiment
        )
        
        decision, explanation, suggested_limit, interest_rate = calculate_loan_recommendation(composite_score, request.revenue)
        
        return {
            "final_credit_score": composite_score,
            "risk_level": risk_level,
            "decision": decision,
            "explanation": explanation,
            "suggested_limit": suggested_limit,
            "interest_rate": interest_rate
        }
    except Exception as e:
        print(f"Error in simulate_credit: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cam")
async def generate_cam(request: Request):
    print(f"DEBUG: Received Report Generation Request")
    
    try:
        request_data = await request.json()
    except:
        request_data = {}

    # Use passed data if available, otherwise fallback to state
    if request_data and len(request_data) > 0:
        data = request_data
    elif hasattr(app.state, 'last_analysis'):
        data = app.state.last_analysis
    else:
        raise HTTPException(status_code=400, detail="No analysis data provided or found in state.")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_name = f"CAM_Report_{timestamp}.pdf"
    output_path = os.path.join(REPORT_DIR, report_name)
    
    # Partition data for 10-section generator
    financials = {
        "revenue": data.get("revenue", 0),
        "debt": data.get("debt", 0),
        "profit": data.get("profit", 0),
        "assets": data.get("assets", 0),
        "meta": data.get("meta", {})
    }
    
    risk_data = {
        "risk_score": data.get("final_credit_score"),
        "risk_level": data.get("risk_level"),
        "decision": data.get("decision"),
        "explanation": data.get("explanation"),
        "ratios": data.get("ratios"),
        "news_level": data.get("news_level"),
        "news_narrative": data.get("news_narrative"),
        "news_flags": data.get("news_flags", []),
        "promoter_risk": data.get("promoter_risk"),
        "liquidity_risk": data.get("liquidity_risk"),
        "ews": data.get("ews"),
        "credit_notes": data.get("credit_notes"),
        "financial_insight": data.get("financial_insight"),
        "promoter_insight": data.get("promoter_insight"),
        "liquidity_insight": data.get("liquidity_insight"),
        "ews_insight": data.get("ews_insight"),
        "reputation_insight": data.get("reputation_insight"),
        "validation_flags": data.get("validation_flags", []),
        "suggested_limit": data.get("suggested_limit"),
        "interest_rate": data.get("interest_rate"),
        "meta": data.get("meta")
    }
    
    try:
        success = generate_cam_report(financials, risk_data, output_path)
        if not success:
             raise Exception("Report generator returned False without exception")
    except Exception as e:
        import traceback
        error_msg = f"PDF Engine Crash: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    
    return {
        "message": "CAM report generated",
        "file": report_name,
        "path": f"/reports/{report_name}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
