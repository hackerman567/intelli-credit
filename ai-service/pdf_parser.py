import pdfplumber
import os
import re

def extract_financial_data(pdf_path):
    """
    Extracts financial keywords and their corresponding values from a PDF.
    """
    data = {
        "revenue": 0,
        "debt": 0,
        "profit": 0,
        "assets": 0
    }

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return data

    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            # Clean text for better matching
            full_text = full_text.lower()

            # Simple regex patterns for demonstration
            # In a real MNC style, this would be more robust (using NLP or table extraction)
            patterns = {
                "revenue": r"revenue[:\s]*\$?([\d,.]+)",
                "debt": r"debt[:\s]*\$?([\d,.]+)",
                "profit": r"profit[:\s]*\$?([\d,.]+)",
                "assets": r"assets[:\s]*\$?([\d,.]+)"
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, full_text)
                if match:
                    # Remove commas and convert to float
                    value_str = match.group(1).replace(",", "")
                    try:
                        data[key] = float(value_str)
                    except ValueError:
                        data[key] = 0

            return data

    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return data
