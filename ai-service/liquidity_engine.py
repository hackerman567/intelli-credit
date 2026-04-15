def analyze_liquidity_stress(financials):
    """
    Detects liquidity stress and high leverage patterns.
    Analyzes ability to meet debt obligations from revenue and profit.
    """
    revenue = financials.get("revenue", 0)
    debt = financials.get("debt", 0)
    profit = financials.get("profit", 0)

    if revenue == 0:
        return {
            "debt_ratio": 0,
            "profit_margin": 0,
            "liquidity_score": 0,
            "liquidity_risk_level": "Severe Liquidity Risk",
            "flags": ["No revenue detected; extreme liquidity risk"]
        }

    # Calculations
    debt_ratio = round(debt / revenue, 2)
    profit_margin = round(profit / revenue, 4)

    score = 100
    flags = []

    # Risk Rules & Penalties
    if debt_ratio > 1.0:
        score -= 30
        flags.append("Debt exceeds total annual revenue (Critical leverage)")
    elif debt_ratio > 0.8:
        score -= 20
        flags.append("High leverage risk (Debt > 80% of revenue)")

    if profit_margin < 0.02:
        score -= 25
        flags.append("Severe liquidity stress (Profit margin below 2%)")
    elif profit_margin < 0.05:
        score -= 15
        flags.append("Low profitability (Margin below 5%)")

    # Clamp score
    score = max(0, min(100, score))

    # Risk Classification
    risk_level = "Severe Liquidity Risk"
    if score >= 75:
        risk_level = "Healthy"
    elif score >= 50:
        risk_level = "Moderate Stress"

    return {
        "debt_ratio": debt_ratio,
        "profit_margin": round(profit_margin * 100, 2),
        "liquidity_score": score,
        "liquidity_risk_level": risk_level,
        "flags": flags
    }
