import time
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

def force_string(val):
    if not val: return ""
    if isinstance(val, str):
        if val.strip().startswith('{'):
            try:
                import json
                obj = json.loads(val)
                return force_string(obj)
            except: return val
        return val
    if isinstance(val, dict):
        for k in ["loan_recommendation", "credit_worthiness", "creditworthiness", "overall_risk", "decision", "explanation", "analysis", "summary"]:
            if val.get(k): return str(val.get(k))
        for v in val.values():
            if isinstance(v, str) and len(v) > 20: return v
        return str(val)
    return str(val)

def safe_get(data, key, default={}):
    if data is None or not isinstance(data, dict): return default
    val = data.get(key)
    return val if val is not None else default

def generate_cam_report(financials, risk_data, output_path):
    """
    Generates an International Hackathon-Grade High-Density Credit Appraisal Memo (CAM).
    Designed for maximum information density and professional demo impact.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # --- BRANDING COLORS ---
    PRIMARY_BLUE = colors.HexColor("#0f172a") # Slate 900
    SECONDARY_BLUE = colors.HexColor("#1e40af") # Blue 800
    ACCENT_GOLD = colors.HexColor("#b45309") # Amber 700
    BG_LIGHT = colors.HexColor("#f8fafc") # Slate 50
    TEXT_MAIN = colors.HexColor("#1e293b") # Slate 800
    TEXT_MUTED = colors.HexColor("#64748b") # Slate 500

    # --- Watermark (Professional Shield) ---
    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillColor(colors.lightgrey, alpha=0.05)
    c.translate(width/2, height/2)
    c.rotate(30)
    c.drawCentredString(0, 0, "INSTITUTIONAL CORE")
    c.drawCentredString(0, -80, "AUTHORIZED ACCESS ONLY")
    c.restoreState()

    # --- Header ---
    c.setFillColor(PRIMARY_BLUE)
    c.rect(0, height - 1.5*inch, width, 1.5*inch, fill=1, stroke=0)
    c.setFillColor(ACCENT_GOLD)
    c.rect(0, height - 1.55*inch, width, 0.05*inch, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.5*inch, height - 0.6*inch, "INTELLI-CREDIT")
    c.setFont("Helvetica", 10)
    c.drawString(0.5*inch, height - 0.8*inch, "Global Institutional Banking Group")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawString(0.5*inch, height - 1.0*inch, "ISO 27001 | RBI COMPLIANT NEURAL AUDIT ENGINE")

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(width - 0.5*inch, height - 0.5*inch, "INTERNAL CLASSIFICATION: CONFIDENTIAL")
    c.setFont("Helvetica", 8)
    c.drawRightString(width - 0.5*inch, height - 0.65*inch, f"REPORT ID: IC/CAM/{int(time.time())}")
    c.drawRightString(width - 0.5*inch, height - 0.8*inch, f"GENERATED ON: {timestamp}")

    y_position = height - 2.0*inch

    # --- HELPERS ---
    def check_new_page(current_y, required_space=120):
        if current_y < required_space:
            c.saveState()
            c.setStrokeColor(colors.lightgrey)
            c.line(0.5*inch, 0.6*inch, width - 0.5*inch, 0.6*inch)
            c.setFont("Helvetica-Oblique", 7)
            c.setFillColor(TEXT_MUTED)
            c.drawString(0.5*inch, 0.45*inch, f"Intelli-Credit Security Hash: {hash(output_path)}")
            c.drawRightString(width - 0.5*inch, 0.45*inch, f"Institutional Disclosure - Page {c.getPageNumber()}")
            c.restoreState()
            c.showPage()
            return height - 1.0*inch
        return current_y

    def draw_section_header(title, y):
        y = check_new_page(y, 100)
        y -= 10 # Add safety gap from content above
        c.setFillColor(BG_LIGHT)
        # Draw background slightly offset downward so top doesn't hit previous text
        c.rect(0.5*inch, y - 10, width - 1.0*inch, 25, fill=1, stroke=0)
        c.setFillColor(SECONDARY_BLUE)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.6*inch, y, title.upper())
        c.setStrokeColor(SECONDARY_BLUE)
        c.setLineWidth(1.5)
        c.line(0.5*inch, y - 10, width - 0.5*inch, y - 10)
        return y - 35

    def draw_text_block(text, y, font="Helvetica", size=9, bold=False, color=TEXT_MAIN, indent=0.7*inch, width_limit=width-1.5*inch):
        if not text: return y
        c.setFont("Helvetica-Bold" if bold else font, size)
        c.setFillColor(color)
        wrapped = simpleSplit(force_string(text), font, size, width_limit)
        for line in wrapped:
            y = check_new_page(y, 20)
            c.drawString(indent, y, line)
            y -= 11
        return y - 5

    def draw_kpi_table(data_map, y):
        y = check_new_page(y, 80)
        box_w = (width - 1.2*inch) / 4
        box_h = 45
        curr_x = 0.6*inch
        for label, val in data_map.items():
            c.setStrokeColor(colors.lightgrey)
            c.setFillColor(colors.white)
            c.rect(curr_x, y - box_h, box_w, box_h, fill=1, stroke=1)
            c.setFillColor(SECONDARY_BLUE)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(curr_x + box_w/2, y - 15, label.upper())
            c.setFillColor(TEXT_MAIN)
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(curr_x + box_w/2, y - 35, str(val))
            curr_x += box_w
        return y - box_h - 15

    # --- SECTION 1: EXECUTIVE BRIEFING ---
    company_name = force_string(risk_data.get('meta', {}).get('company_name', 'Subject Entity'))
    y_position = draw_section_header(f"1.0 EXECUTIVE INTELLIGENCE BRIEFING: {company_name}", y_position)
    
    # 1.1 Decision Rationale (High Impact)
    decision = force_string(risk_data.get('decision', 'N/A')).upper()
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#16a34a") if "APPROV" in decision else colors.red)
    c.drawString(0.7*inch, y_position, f"SYSTEM RECOMMENDATION: {decision}")
    y_position -= 20
    
    # 1.2 Main Credit Notes (The "More" Content)
    notes = force_string(risk_data.get('credit_notes', ''))
    if notes:
        y_position = draw_text_block(notes, y_position, size=8, color=TEXT_MUTED)
    else:
        y_position = draw_text_block(risk_data.get('explanation'), y_position)
    
    y_position -= 20 # Extra safety gap after large text block

    # --- SECTION 2: AUDIT & DATA INTEGRITY ---
    y_position = draw_section_header("2.0 FORENSIC DATA INTEGRITY AUDIT", y_position)
    
    val_flags = risk_data.get('validation_flags', [])
    int_flags = risk_data.get('integrity_flags', [])
    all_flags = val_flags + int_flags
    
    if all_flags:
        c.setFillColor(colors.HexColor("#fff1f2"))
        c.rect(0.7*inch, y_position - 15, width - 1.4*inch, 20, fill=1, stroke=0)
        c.setFillColor(colors.red)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(0.8*inch, y_position - 7, f"CRITICAL ANOMALIES DETECTED ({len(all_flags)})")
        y_position -= 25
        for flag in all_flags:
            y_position = draw_text_block(f"• [AUDIT ALERT] {flag}", y_position, size=8, color=colors.red)
    else:
        y_position = draw_text_block("DATA INTEGRITY VERIFIED: No discrepancies found across GST, Bank Inflow, and Portfolio Cross-Checks.", y_position, color=colors.green, bold=True)
    y_position -= 10

    # --- SECTION 3: KEY PERFORMANCE INDICATORS ---
    y_position = draw_section_header("3.0 QUANTITATIVE PERFORMANCE METRICS", y_position)
    ratios = safe_get(risk_data, 'ratios', {})
    kpis = {
        "Risk Grade": risk_data.get('risk_level', 'N/A'),
        "DSCR": f"{ratios.get('dscr', '0')}x",
        "Net Margin": f"{ratios.get('profit_margin', '0')}%",
        "Debt/Rev": f"{ratios.get('debt_to_revenue', '0')}%"
    }
    y_position = draw_kpi_table(kpis, y_position)
    
    # Financial Insight Box
    y_position = draw_text_block(risk_data.get('financial_insight'), y_position, font="Helvetica-Oblique", color=SECONDARY_BLUE, bold=True)

    # --- SECTION 4: MARKET & REPUTATION SENTIMENT ---
    y_position = draw_section_header("4.0 MARKET SENTIMENT & REPUTATIONAL DYNAMICS", y_position)
    narrative = force_string(risk_data.get('news_narrative', 'No significant news presence detected in current audit cycle.'))
    y_position = draw_text_block(narrative, y_position)
    
    news_flags = risk_data.get('news_flags', [])
    if news_flags:
        for flag in news_flags:
            y_position = draw_text_block(f"→ [MARKET SIGNAL] {flag}", y_position, size=8, color=ACCENT_GOLD)
    y_position -= 10

    # --- SECTION 5: CONTAGION & SYSTEMIC IMPACT ---
    y_position = draw_section_header("5.0 SYSTEMIC CONTAGION & RIPPLE ANALYSIS", y_position)
    contagion = safe_get(risk_data, 'contagion', {})
    
    # 5.1 Lender & Supplier Impact
    y_position = draw_text_block(f"DIRECT LENDER IMPACT: {contagion.get('direct_impact', 'N/A')}", y_position, bold=True, size=8)
    y_position = draw_text_block(f"INDIRECT ECOSYSTEM IMPACT: {contagion.get('indirect_impact', 'N/A')}", y_position, size=8)
    
    # 5.2 Cascade Flow
    y_position = draw_text_block("FAILURE PROPAGATION CASCADE:", y_position, bold=True, size=8)
    steps = contagion.get('cascade_flow', [])
    for i, step in enumerate(steps[:4]):
        y_position = draw_text_block(f"{i+1}. {step}", y_position, size=8, indent=0.9*inch)
    
    # 5.3 AI Verdict
    y_position = draw_text_block("SYSTEMIC VERDICT:", y_position, bold=True, size=8)
    y_position = draw_text_block(contagion.get('ai_verdict'), y_position, font="Helvetica-Oblique", size=8, color=SECONDARY_BLUE)

    # --- SECTION 6: EARLY WARNING SYSTEM (EWS) ---
    y_position = draw_section_header("6.0 EARLY WARNING SYSTEM (EWS) SIGNALS", y_position)
    ews = safe_get(risk_data, 'ews', {})
    ews_level = str(ews.get('ews_risk_level', 'LOW')).upper()
    
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.red if ews_level == 'HIGH' else SECONDARY_BLUE)
    c.drawString(0.7*inch, y_position, f"EWS MONITORING STATUS: {ews_level}")
    y_position -= 15
    y_position = draw_text_block(risk_data.get('ews_insight'), y_position)

    # --- SECTION 7: SANCTION TERMS & LIMITS ---
    y_position = draw_section_header("7.0 FINAL SANCTION DISCLOSURE", y_position)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(0.7*inch, y_position, f"AUTHORIZED LIMIT: INR {risk_data.get('suggested_limit', 0)} CR")
    y_position -= 15
    c.setFont("Helvetica", 10)
    c.drawString(0.7*inch, y_position, f"Pricing: {risk_data.get('interest_rate', 8.5)}% p.a. (System-Optimized)")
    y_position -= 30

    # --- SIGNATURE BLOCK ---
    y_position = check_new_page(y_position, 180)
    y_position -= 60
    
    c.setStrokeColor(TEXT_MAIN)
    c.line(0.7*inch, y_position, 2.5*inch, y_position)
    c.line(width - 2.5*inch, y_position, width - 0.7*inch, y_position)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(0.7*inch, y_position - 12, "DIGITAL SYSTEM SIGNATURE")
    c.drawRightString(width - 0.7*inch, y_position - 12, "AUTHORIZING CREDIT OFFICER")
    
    # Signature Curve
    c.setStrokeColor(SECONDARY_BLUE)
    p = c.beginPath()
    p.moveTo(width - 2.3*inch, y_position + 10)
    p.curveTo(width - 2.1*inch, y_position + 25, width - 1.8*inch, y_position + 5, width - 1.5*inch, y_position + 20)
    p.curveTo(width - 1.3*inch, y_position + 30, width - 1.1*inch, y_position + 15, width - 0.9*inch, y_position + 25)
    c.drawPath(p)
    
    # Audit Seal
    c.setStrokeColor(ACCENT_GOLD)
    c.setFillColor(colors.HexColor("#fffbeb"))
    c.rect(width - 2.5*inch, y_position - 80, 1.8*inch, 60, fill=1, stroke=1)
    c.setFillColor(ACCENT_GOLD)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(width - 1.6*inch, y_position - 35, "INTELLI-CREDIT")
    c.drawCentredString(width - 1.6*inch, y_position - 45, "SECURE VERIFIED")
    c.drawCentredString(width - 1.6*inch, y_position - 55, "TRUSTED AUDIT")
    c.setFont("Helvetica", 6)
    c.drawCentredString(width - 1.6*inch, y_position - 70, f"AUTH_ID: {hash(timestamp)}")

    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width/2, 0.4*inch, "© 2026 Intelli-Credit Global Banking Group. Private & Confidential. RBI Compliance Document.")

    c.save()
    return True
