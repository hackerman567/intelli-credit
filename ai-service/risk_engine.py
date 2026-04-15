from liquidity_engine import analyze_liquidity_stress
from promoter_risk import evaluate_promoter_risk
from ews_engine import analyze_ews

def calculate_risk_score(financials):
    """
    Base Rules-based scoring engine for corporate credit appraisal.
    """
    revenue = financials.get("revenue", 0)
    debt = financials.get("debt", 0)
    profit = financials.get("profit", 0)
    assets = financials.get("assets", 0)

    score = 0

    # Revenue Rule
    if revenue > 50:
        score += 30
    elif revenue > 20:
        score += 15

    # Debt-to-Revenue Rule
    if revenue > 0:
        if debt < (0.5 * revenue):
            score += 30
        elif debt < revenue:
            score += 15
        else:
            score -= 10
    else:
        score -= 20

    # Profitability Rule
    if profit > 10:
        score += 20
    elif profit > 5:
        score += 10
    elif profit < 0:
        score -= 20

    # Asset Coverage Rule
    if assets > debt:
        score += 20
    else:
        score -= 10

    score = max(0, min(100, score))
    return score

def get_risk_level(score):
    """
    Banking-grade risk classification logic with Indian Context.
    """
    if score > 85:
        return "Low Risk (Elite)"
    elif score > 70:
        return "Low Risk (Standard)"
    elif score >= 55:
        return "Moderate Risk"
    elif score >= 40:
        return "High Risk (Monitoring Required)"
    else:
        return "Critical Risk (Likely NPAs)"

def calculate_five_cs(financials, ratios, promoter_results, news_penalty, officer_sentiment=0, network_penalty=0):
    """
    Groups scoring into the 5 pillars of banking credit appraisal.
    """
    # 1. CHARACTER (Integrity & Governance)
    promoter_score = promoter_results.get("promoter_risk_score", 50)
    # Apply Network Penalty to Character
    character_score = max(0, min(100, promoter_score + (officer_sentiment * 10) + network_penalty))
    
    # 2. CAPACITY (Repayment Ability)
    dscr = ratios.get("dscr", 1.0)
    d_to_r = ratios.get("debt_to_revenue", 1.0)
    # Target DSCR > 1.25, Target DtoR < 0.5
    capacity_score = 0
    if dscr > 1.5: capacity_score += 60
    elif dscr > 1.0: capacity_score += 40
    if d_to_r < 0.4: capacity_score += 40
    elif d_to_r < 0.8: capacity_score += 20
    
    # 3. CAPITAL (Financial Reserves)
    margin = ratios.get("profit_margin", 0)
    capital_score = 0
    if margin > 15: capital_score = 100
    elif margin > 8: capital_score = 75
    elif margin > 0: capital_score = 50
    else: capital_score = 20
    
    # 4. COLLATERAL (Security Coverage)
    assets = financials.get("assets", 0)
    debt = financials.get("debt", 0)
    collateral_score = min(100, (assets / debt * 50)) if debt > 0 else 100
    
    # 5. CONDITIONS (Market & External)
    # Base 70, adjusted by news and sector
    conditions_score = max(0, min(100, 70 + news_penalty))
    
    return {
        "character": round(character_score, 1),
        "capacity": round(capacity_score, 1),
        "capital": round(capital_score, 1),
        "collateral": round(collateral_score, 1),
        "conditions": round(conditions_score, 1)
    }

def get_composite_risk_score(pillar_scores):
    """
    Weights the 5 pillars to produce a final banking-grade score.
    Character (20%), Capacity (30%), Capital (20%), Collateral (15%), Conditions (15%)
    """
    weighted_score = (
        pillar_scores["character"] * 0.20 +
        pillar_scores["capacity"] * 0.30 +
        pillar_scores["capital"] * 0.20 +
        pillar_scores["collateral"] * 0.15 +
        pillar_scores["conditions"] * 0.15
    )
    
    final_score = round(max(0, min(100, weighted_score)), 1)
    return final_score, get_risk_level(final_score)

def calculate_loan_recommendation(score, revenue):
    """
    Implements Pillar 3: Suggests Loan Limit & Interest Rate based on Risk Core.
    """
    risk_premium = (100 - score) / 5
    interest_rate = 8.5 + risk_premium
    
    limit_multiplier = (score / 100) * 0.2
    suggested_limit = round(revenue * limit_multiplier, 2)

    if score > 75:
        decision = "Preferred Approval"
        explanation = f"Elite credit profile (5Cs verified). Proposal for limit of INR {suggested_limit} Cr at {interest_rate:.2f}% ROI (Standard rate)."
    elif score >= 55:
        decision = "Approval"
        explanation = f"Solid banking credentials. Recommended limit of INR {suggested_limit} Cr at {interest_rate:.2f}% ROI with periodic monitoring."
    elif score >= 40:
        decision = "Conditional Sanction"
        explanation = "Moderate weaknesses in 5Cs (likely Capacity or Conditions). Requires additional 25% collateral haircut."
    else:
        decision = "Declined"
        explanation = "High Probability of Default detected. Financial capacity does not support the requested credit exposure."

    return decision, explanation, suggested_limit, round(interest_rate, 2)
