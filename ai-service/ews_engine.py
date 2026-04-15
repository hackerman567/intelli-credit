def analyze_ews(financial_score, liquidity_score, promoter_score, news_risk=False, extra_data=None):
    """
    Early Warning System: Predicts default probability using specific signals.
    Returns probability between 5% and 85%.
    """
    # Start with a base probability
    default_probability = 15 
    signals = []
    observation = "No major financial distress indicators detected."

    if extra_data:
        try:
            debt_ratio = float(str(extra_data.get('debt_ratio', 0)).replace('%', ''))
            profit_margin = float(str(extra_data.get('profit_margin', 0)).replace('%', ''))
            
            # Rule 1: High Debt to Revenue Ratio
            if debt_ratio > 0.8:
                default_probability += 35
                signals.append("High leverage risk detected (Debt > 80% of revenue)")
            elif debt_ratio > 0.5:
                default_probability += 15
                signals.append("Elevated leverage observation")

            # Rule 2: Low Profit Margin
            if profit_margin < 5:
                default_probability += 25
                signals.append("Profitability concern (Margin < 5%)")
                observation = "Thin profit margins indicate low absorption capacity for market shocks."
            elif profit_margin < 10:
                default_probability += 10
                signals.append("Moderate profitability pressure")

        except (ValueError, TypeError):
            pass

    # Adjustment for other scores
    if financial_score < 50:
        default_probability += 10
    if news_risk:
        default_probability += 15
        observation = "Adverse news signals combined with financial profiles suggest heightened monitoring."

    # Clamp probability between 5% and 85%
    default_probability = max(5, min(85, default_probability))

    # Risk Level
    if default_probability >= 60:
        level = "High Default Risk"
    elif default_probability >= 30:
        level = "Moderate Default Risk"
    else:
        level = "Low Default Risk"

    return {
        "default_probability": default_probability,
        "ews_risk_level": level,
        "signals": signals,
        "observation": observation
    }
