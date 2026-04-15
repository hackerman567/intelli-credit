def calculate_ratios(financials):
    """
    Calculates key financial ratios for bank credit appraisal.
    """
    revenue = financials.get("revenue", 0)
    debt = financials.get("debt", 0)
    profit = financials.get("profit", 0)

    ratios = {
        "debt_to_revenue": 0,
        "profit_margin": 0
    }

    if revenue > 0:
        ratios["debt_to_revenue"] = round(debt / revenue, 2)
        ratios["profit_margin"] = round((profit / revenue) * 100, 2)
    
    # Forensic DSCR: Debt Service Coverage Ratio
    # Real-world benchmark: Need > 1.25 for loan approval
    estimated_installment = debt * 0.12 # Assume 12% annual repayment (Principal + Interest)
    if estimated_installment > 0:
        ratios["dscr"] = round(profit / estimated_installment, 2)
    else:
        ratios["dscr"] = 3.0 # High adequacy if no debt

    return ratios
