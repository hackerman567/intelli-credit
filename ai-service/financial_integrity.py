def financial_integrity_check(financial_data):
    """
    Detects suspicious financial patterns like inflated sales or circular trading.
    Compares Revenue vs Bank Inflow vs GST Sales.
    """
    revenue = financial_data.get("revenue", 0)
    bank_inflow = financial_data.get("bank_inflow", 0)
    gst_sales = financial_data.get("gst_sales", 0)

    penalty_score = 0
    integrity_flags = []

    if revenue == 0:
        return 0, []

    # Check 1: Revenue vs Bank Inflow (Inflated Sales Check)
    # If reported revenue is significantly higher than actual bank receipts
    if revenue > (bank_inflow * 1.5):
        integrity_flags.append("Revenue significantly higher than bank inflow (possible inflated sales)")
        penalty_score -= 15

    # Check 2: Revenue vs GST Filings (Mismatch Check)
    # If revenue reported to bank is higher than what's reported to tax authorities
    if revenue > (gst_sales * 1.4):
        integrity_flags.append("Revenue inconsistent with GST filings (potential reporting mismatch)")
        penalty_score -= 10

    # Check 3: Circular Trading Detection
    # Pattern: Bank inflow and GST sales match, but Revenue is pushed artificially high
    if abs(bank_inflow - gst_sales) < (0.1 * gst_sales) and revenue > (bank_inflow * 1.6):
        integrity_flags.append("Possible circular trading pattern detected (High Revenue vs Activity)")
        penalty_score -= 20

    return penalty_score, integrity_flags
