import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def analyze_news(company_name):
    """
    Fetches top 5 news articles using NewsAPI and detects risk keywords.
    Returns risk level (Low/Moderate/High) and a short narrative.
    """
    if not NEWS_API_KEY:
        return 0, ["News API Key missing"], "Low Risk", "Reputation scan skipped due to missing API key."

    try:
        url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=relevancy&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        articles = response.json().get('articles', [])
        
        risk_keywords = ["fraud", "scam", "investigation", "corruption", "default"]
        found_flags = []
        severity = 0

        for art in articles:
            content = (art.get('title', '') + " " + art.get('description', '')).lower()
            for kw in risk_keywords:
                if kw in content:
                    flag = f"Adverse News: '{kw}' mentioned in {art['source']['name']}"
                    if flag not in found_flags:
                        found_flags.append(flag)
                        severity += 1

        if severity >= 3:
            level = "High Risk"
            narrative = f"Critical reputational risk detected with {severity} adverse mentions found in recent media reports."
            penalty = -25
        elif severity >= 1:
            level = "Moderate Risk"
            narrative = f"Moderate reputational concern identified. {severity} adverse mention(s) found regarding regulatory or legal keywords."
            penalty = -10
        else:
            level = "Low Risk"
            narrative = "No significant adverse news or reputational risks detected in live media scan."
            penalty = 0
        
        return penalty, found_flags, level, narrative

    except Exception as e:
        print(f"NewsAPI error: {e}")
        return 0, ["News system API Error"], "Low Risk", "Reputation check incomplete due to technical failure."
