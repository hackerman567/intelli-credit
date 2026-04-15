def evaluate_promoter_risk(promoter_name, director_profile):
    """
    Evaluates management quality and governance risk based on director track record.
    Follows banking standards for 'Character' assessment in the 5Cs of Credit.
    """
    if not director_profile:
        return {
            "promoter_risk_score": 100,
            "governance_risk_level": "Low",
            "flags": ["No director profile data provided; assuming clean record."]
        }

    total_companies = director_profile.get("total_companies", 0)
    closed_companies = director_profile.get("closed_companies", 0)
    legal_cases = director_profile.get("legal_cases", 0)
    active_companies = director_profile.get("active_companies", 0)

    score = 100
    flags = []

    # Risk Deductions
    if closed_companies >= 2:
        score -= 20
        flags.append("Promoter associated with multiple closed companies (Possible failure history)")

    if legal_cases >= 1:
        score -= 25
        flags.append("Promoter involved in legal disputes or litigation")

    if total_companies > 10:
        score -= 10
        flags.append("Promoter involved in unusually high number of companies (Potential over-leveraged focus)")

    # Clamp score
    score = max(0, min(100, score))

    # Risk Classification
    risk_level = "High"
    if score >= 75:
        risk_level = "Low"
    elif score >= 50:
        risk_level = "Medium"

    return {
        "promoter_name": promoter_name,
        "promoter_risk_score": score,
        "governance_risk_level": risk_level,
        "flags": flags
    }
